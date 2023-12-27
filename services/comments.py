import httpx
from config.config import settings

# Get a comment from Regulations.gov API 
async def get_comment(comment_id):
    regulations_api_key = settings.REGULATIONS_API_KEY
    async with httpx.AsyncClient() as client:
        comment_api = f"https://api.regulations.gov/v4/documents/{comment_id}?include=attachments&api_key={regulations_api_key}"
        response = await client.get(comment_api)
        return response
    