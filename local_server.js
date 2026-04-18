const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = process.cwd();

const sendJson = (res, statusCode, payload) => {
    res.writeHead(statusCode, {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'no-store',
    });
    res.end(JSON.stringify(payload));
};

const getExpectedAccessToken = () => {
    return process.env.ARTICLE_JIKE_ACCESS_TOKEN || process.env.APP_ACCESS_TOKEN || '';
};

const getRequestAccessToken = (req, data = {}) => {
    const headerToken = req.headers['x-article-jike-access-token'];
    const authHeader = req.headers.authorization || '';
    const bearerMatch = authHeader.match(/^Bearer\s+(.+)$/i);
    return String(headerToken || (bearerMatch && bearerMatch[1]) || data.accessToken || '').trim();
};

const validateAccessToken = (req, res, data) => {
    const expected = getExpectedAccessToken();
    if (!expected) return true;
    if (getRequestAccessToken(req, data) === expected) return true;
    sendJson(res, 401, { error: 'Unauthorized', code: 'ACCESS_TOKEN_REQUIRED' });
    return false;
};

// 1. Load .env.local manually
try {
    const envContent = fs.readFileSync('.env.local', 'utf8');
    envContent.split('\n').forEach(line => {
        const match = line.match(/^([^=]+)=(.*)$/);
        if (match) {
            const key = match[1].trim();
            const value = match[2].trim();
            process.env[key] = value;
        }
    });
    console.log('Loaded .env.local');
} catch (e) {
    console.warn('No .env.local found');
}

// 2. Proxy Logic (Copied and adapted from api/proxy.js)
const handleProxy = async (req, res) => {
    if (req.method !== 'POST') {
        res.statusCode = 405;
        res.end(JSON.stringify({ error: 'Method Not Allowed' }));
        return;
    }

    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', async () => {
        try {
            const data = JSON.parse(body);
            if (!validateAccessToken(req, res, data)) return;

            const baseUrl = data.baseUrl || process.env.OPENAI_BASE_URL || process.env.NEWAPI_BASE_URL || 'https://api.openai.com/v1';
            const apiKey = data.apiKey || process.env.OPENAI_API_KEY || process.env.NEWAPI_API_KEY;
            const model = data.model || process.env.OPENAI_MODEL || process.env.NEWAPI_MODEL || 'gpt-5.4';
            const messages = data.messages;
            const isStream = data.stream === true;

            console.log('[Local Proxy]', { baseUrl, hasApiKey: !!apiKey, model, isStream });

            if (!baseUrl || !apiKey || !model || !Array.isArray(messages)) {
                res.statusCode = 400;
                res.end(JSON.stringify({ error: 'Bad Request' }));
                return;
            }

            const endpoint = baseUrl.endsWith('/') ? `${baseUrl}chat/completions` : `${baseUrl}/chat/completions`;
            
            const payload = { model, messages, stream: isStream };
            if (data.reasoning_effort !== undefined) {
                payload.reasoning_effort = data.reasoning_effort;
            } else if (process.env.OPENAI_REASONING_EFFORT) {
                payload.reasoning_effort = process.env.OPENAI_REASONING_EFFORT;
            }

            for (const key of ['max_tokens', 'max_completion_tokens', 'temperature', 'top_p']) {
                if (data[key] !== undefined) payload[key] = data[key];
            }

            const upstream = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`,
                },
                body: JSON.stringify(payload),
            });

            res.statusCode = upstream.status;
            res.setHeader('Content-Type', upstream.headers.get('content-type') || 'application/json');
            
            if (isStream && upstream.body) {
                // Stream using standard ReadableStream (Node 18+)
                // Or adapt for Node < 18 if needed, but assuming modern Node here based on env
                const reader = upstream.body.getReader();
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    res.write(value);
                }
                res.end();
            } else {
                const text = await upstream.text();
                res.end(text);
            }

        } catch (e) {
            console.error(e);
            res.statusCode = 500;
            res.end(JSON.stringify({ error: e.message }));
        }
    });
};

// 3. Static File Server
const server = http.createServer((req, res) => {
    console.log(`${req.method} ${req.url}`);

    let pathname;
    try {
        pathname = decodeURIComponent(new URL(req.url, `http://${req.headers.host || 'localhost'}`).pathname);
    } catch (e) {
        res.writeHead(400);
        res.end('Bad Request');
        return;
    }

    // Lightweight health check for deployments.
    if (pathname === '/api/status') {
        const expectedAccessToken = getExpectedAccessToken();
        return sendJson(res, 200, {
            ok: true,
            service: 'article-jike',
            model: process.env.OPENAI_MODEL || process.env.NEWAPI_MODEL || 'gpt-5.4',
            reasoningEffort: process.env.OPENAI_REASONING_EFFORT || null,
            accessControl: Boolean(expectedAccessToken),
            authorized: !expectedAccessToken || getRequestAccessToken(req) === expectedAccessToken,
            serverKeyConfigured: Boolean(process.env.OPENAI_API_KEY || process.env.NEWAPI_API_KEY),
            uptimeSeconds: Math.round(process.uptime()),
            serverTime: new Date().toISOString(),
        });
    }

    // Route to Proxy
    if (pathname === '/api/proxy') {
        return handleProxy(req, res);
    }

    // Default to index
    if (pathname === '/') pathname = '/wechat_workflow.html';

    const filePath = path.resolve(ROOT_DIR, `.${pathname}`);
    if (!filePath.startsWith(`${ROOT_DIR}${path.sep}`)) {
        res.writeHead(403);
        res.end('Forbidden');
        return;
    }

    const extname = path.extname(filePath);
    let contentType = 'text/html; charset=utf-8';
    switch (extname) {
        case '.js': contentType = 'text/javascript; charset=utf-8'; break;
        case '.css': contentType = 'text/css; charset=utf-8'; break;
        case '.json': contentType = 'application/json; charset=utf-8'; break;
        case '.md': contentType = 'text/markdown; charset=utf-8'; break;
        case '.png': contentType = 'image/png'; break;
        case '.jpg': contentType = 'image/jpg'; break;
    }

    fs.readFile(filePath, (error, content) => {
        if (error) {
            if(error.code == 'ENOENT'){
                res.writeHead(404);
                res.end('404 Not Found');
            } else {
                res.writeHead(500);
                res.end('Sorry, check with the site admin for error: '+error.code+' ..\n');
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

const PORT = Number(process.env.PORT || 3001);
const HOST = process.env.HOST || '0.0.0.0';
server.listen(PORT, HOST, () => {
    console.log(`Server running at http://${HOST}:${PORT}/`);
    console.log(`Using API Base: ${process.env.OPENAI_BASE_URL || process.env.NEWAPI_BASE_URL || 'https://api.openai.com/v1'}`);
});
