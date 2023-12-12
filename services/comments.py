import httpx
from config.config import settings

# Fetch a comment from Regulations.gov API 
async def fetch_comment(comment_id):
    api_key = settings.API_KEY
    async with httpx.AsyncClient() as client:
        comment_api = f"https://api.regulations.gov/v4/documents/{comment_id}?include=attachments&api_key={api_key}"
        response = await client.get(comment_api)
        return response
    