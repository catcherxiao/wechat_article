const getExpectedAccessToken = () => {
  return process.env.ARTICLE_JIKE_ACCESS_TOKEN || process.env.APP_ACCESS_TOKEN || ''
}

const getRequestAccessToken = (req, body = {}) => {
  const headerToken = req.headers['x-article-jike-access-token']
  const authHeader = req.headers.authorization || ''
  const bearerMatch = authHeader.match(/^Bearer\s+(.+)$/i)
  return String(headerToken || (bearerMatch && bearerMatch[1]) || body.accessToken || '').trim()
}

const validateAccessToken = (req, res, body) => {
  const expected = getExpectedAccessToken()
  if (!expected) return true
  if (getRequestAccessToken(req, body) === expected) return true

  res.statusCode = 401
  res.setHeader('Content-Type', 'application/json; charset=utf-8')
  res.end(JSON.stringify({ error: 'Unauthorized', code: 'ACCESS_TOKEN_REQUIRED' }))
  return false
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.statusCode = 405
    res.setHeader('Content-Type', 'application/json; charset=utf-8')
    res.end(JSON.stringify({ error: 'Method Not Allowed' }))
    return
  }

  try {
    const { body } = req
    if (!validateAccessToken(req, res, body || {})) return

    const baseUrl = body.baseUrl || process.env.OPENAI_BASE_URL || process.env.NEWAPI_BASE_URL || 'https://api.openai.com/v1'
    const apiKey = body.apiKey || process.env.OPENAI_API_KEY || process.env.NEWAPI_API_KEY
    const model = body.model || process.env.OPENAI_MODEL || process.env.NEWAPI_MODEL || 'gpt-5.4'
    const messages = body.messages

    // Debug Log (will show in Vercel Function Logs)
    console.log('[Proxy Debug]', {
        receivedBodyBaseUrl: body.baseUrl,
        envBaseUrl: process.env.OPENAI_BASE_URL || process.env.NEWAPI_BASE_URL,
        finalBaseUrl: baseUrl,
        hasApiKey: !!apiKey,
        apiKeyLength: apiKey ? apiKey.length : 0,
        model,
        envKeyExists: !!(process.env.OPENAI_API_KEY || process.env.NEWAPI_API_KEY)
    });

    if (!baseUrl || !apiKey || !model || !Array.isArray(messages)) {
      res.statusCode = 400
      res.setHeader('Content-Type', 'application/json; charset=utf-8')
      res.end(JSON.stringify({ 
          error: 'Bad Request: Missing required fields',
          details: {
              hasBaseUrl: !!baseUrl,
              hasApiKey: !!apiKey,
              hasModel: !!model
          }
      }))
      return
    }

    // REMOVED: Domain whitelist check to support custom proxy domains (e.g. yinli.one)
    // const urlObj = new URL(baseUrl)
    // const host = urlObj.hostname
    // const isAllowedHost = host === 'api.newapi.pro' || host.endsWith('.newapi.pro')
    
    const endpoint = baseUrl.endsWith('/') ? `${baseUrl}chat/completions` : `${baseUrl}/chat/completions`
    const isStream = body.stream === true;

    const payload = { model, messages, stream: isStream }
    if (body.reasoning_effort !== undefined) {
      payload.reasoning_effort = body.reasoning_effort
    } else if (process.env.OPENAI_REASONING_EFFORT) {
      payload.reasoning_effort = process.env.OPENAI_REASONING_EFFORT
    }

    for (const key of ['max_tokens', 'max_completion_tokens', 'temperature', 'top_p']) {
      if (body[key] !== undefined) payload[key] = body[key]
    }

    const upstream = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify(payload),
    })

    res.statusCode = upstream.status
    res.setHeader('Content-Type', upstream.headers.get('content-type') || 'application/json; charset=utf-8')

    if (isStream && upstream.body) {
        // Stream the response back to client
        const reader = upstream.body.getReader();
        const encoder = new TextEncoder();
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            res.write(value);
        }
        res.end();
    } else {
        // Non-stream fallback
        const text = await upstream.text()
        res.end(text)
    }
  } catch (e) {
    console.error(e);
    res.statusCode = 500
    res.setHeader('Content-Type', 'application/json; charset=utf-8')
    res.end(JSON.stringify({ error: 'Internal Server Error' }))
  }
}
