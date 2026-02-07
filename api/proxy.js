export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.statusCode = 405
    res.setHeader('Content-Type', 'application/json; charset=utf-8')
    res.end(JSON.stringify({ error: 'Method Not Allowed' }))
    return
  }

  try {
    const { body } = req
    // Default to yinli.one as per user preference
    const baseUrl = body.baseUrl || process.env.NEWAPI_BASE_URL || 'https://yinli.one/v1'
    const apiKey = body.apiKey || process.env.NEWAPI_API_KEY
    const model = body.model
    const messages = body.messages

    // Debug Log (will show in Vercel Function Logs)
    console.log('[Proxy Debug]', {
        receivedBodyBaseUrl: body.baseUrl,
        envBaseUrl: process.env.NEWAPI_BASE_URL,
        finalBaseUrl: baseUrl,
        hasApiKey: !!apiKey,
        apiKeyLength: apiKey ? apiKey.length : 0,
        model,
        envKeyExists: !!process.env.NEWAPI_API_KEY
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

    const upstream = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({ model, messages, stream: isStream }),
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
