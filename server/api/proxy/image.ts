export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  const imageUrl = query.url as string
  console.log('imageUrl', imageUrl);
  
  
  if (!imageUrl) {
    throw createError({
      statusCode: 400,
      message: 'Missing image URL',
    })
  }

  try {
    const response = await fetch(imageUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://movie.douban.com/',
      },
    })

    if (!response.ok) {
      throw createError({
        statusCode: response.status,
        message: `Failed to fetch image: ${response.statusText}`,
      })
    }

    const buffer = await response.arrayBuffer()
    
    setHeaders(event, {
      'Content-Type': response.headers.get('Content-Type') || 'image/jpeg',
      'Cache-Control': 'public, max-age=31536000',
      'Access-Control-Allow-Origin': '*',
    })
    
    return buffer
  } catch (error: any) {
    console.error('Proxy error:', error)
    throw createError({
      statusCode: 500,
      message: `Failed to fetch image: ${error.message}`,
    })
  }
}) 