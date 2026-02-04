const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

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
            const baseUrl = data.baseUrl || process.env.NEWAPI_BASE_URL || 'https://api.newapi.pro/v1';
            const apiKey = data.apiKey || process.env.NEWAPI_API_KEY;
            const model = data.model;
            const messages = data.messages;
            const isStream = data.stream === true;

            console.log('[Local Proxy]', { baseUrl, hasApiKey: !!apiKey, model, isStream });

            if (!baseUrl || !apiKey || !model || !Array.isArray(messages)) {
                res.statusCode = 400;
                res.end(JSON.stringify({ error: 'Bad Request' }));
                return;
            }

            const endpoint = baseUrl.endsWith('/') ? `${baseUrl}chat/completions` : `${baseUrl}/chat/completions`;
            
            const upstream = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`,
                },
                body: JSON.stringify({ model, messages, stream: isStream }),
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

    // Route to Proxy
    if (req.url === '/api/proxy') {
        return handleProxy(req, res);
    }

    // Default to index
    let filePath = '.' + req.url;
    if (filePath === './') filePath = './wechat_workflow.html';

    // Remove query string (e.g. ?ts=123) from file path
    const queryIndex = filePath.indexOf('?');
    if (queryIndex !== -1) {
        filePath = filePath.substring(0, queryIndex);
    }

    const extname = path.extname(filePath);
    let contentType = 'text/html';
    switch (extname) {
        case '.js': contentType = 'text/javascript'; break;
        case '.css': contentType = 'text/css'; break;
        case '.json': contentType = 'application/json'; break;
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

const PORT = 3001;
server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
    console.log(`Using API Base: ${process.env.NEWAPI_BASE_URL}`);
});
