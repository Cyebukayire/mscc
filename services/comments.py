import httpx
api_key = "fUhDOvth3SkvSvVWLym8oJfQHc5CKbHqv92gPanf"

async def fetch_comment(comment_id):
    async with httpx.AsyncClient() as client:
        comment_api = f"https://api.regulations.gov/v4/documents/{comment_id}?include=attachments&api_key={api_key}"
        response = await client.get(comment_api)
        return response
    