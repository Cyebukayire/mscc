import httpx
from config.config import settings
import json

database_path = '../database/comments/database.json'

# Get a comment from Regulations.gov API 
async def get_comment_with_url(comment_id):
    regulations_api_key = settings.REGULATIONS_API_KEY
    async with httpx.AsyncClient() as client:
        comment_api = f"https://api.regulations.gov/v4/documents/{comment_id}?include=attachments&api_key={regulations_api_key}"
        response = await client.get(comment_api)
        return response
    
# Returns the list of all comment objects
async def get_all_comments():
    # Fetch comment objects from database
    with open(database_path, 'r') as db:
        comments = json.load(db)
    return comments

# Returns an object of the comment
async def get_comment(comment_id):
    comments = get_all_comments()
    for comment in comments:
        if comment['data']['id'] == comment_id:
            return {"status": 404, "data": comment}
    
    # Comment not found
    return {"status": 404, "data": None}

