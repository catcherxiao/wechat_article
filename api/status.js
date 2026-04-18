const getExpectedAccessToken = () => {
  return process.env.ARTICLE_JIKE_ACCESS_TOKEN || process.env.APP_ACCESS_TOKEN || ''
}

const getRequestAccessToken = (req) => {
  const headerToken = req.headers['x-article-jike-access-token']
  const authHeader = req.headers.authorization || ''
  const bearerMatch = authHeader.match(/^Bearer\s+(.+)$/i)
  return String(headerToken || (bearerMatch && bearerMatch[1]) || '').trim()
}

export default async function handler(req, res) {
  const expected = getExpectedAccessToken()

  res.statusCode = 200
  res.setHeader('Content-Type', 'application/json; charset=utf-8')
  res.setHeader('Cache-Control', 'no-store')
  res.end(JSON.stringify({
    ok: true,
    service: 'article-jike',
    model: process.env.OPENAI_MODEL || process.env.NEWAPI_MODEL || 'gpt-5.4',
    reasoningEffort: process.env.OPENAI_REASONING_EFFORT || null,
    accessControl: Boolean(expected),
    authorized: !expected || getRequestAccessToken(req) === expected,
    serverKeyConfigured: Boolean(process.env.OPENAI_API_KEY || process.env.NEWAPI_API_KEY),
    serverTime: new Date().toISOString(),
  }))
}
