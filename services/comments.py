import httpx
from config.config import settings
import json
from collections import namedtuple

# namedtuple to format request output
response_data = namedtuple('response', ['status', 'data', 'message'])

database_path = f"{settings.LOCAL_DB_PATH}database.json"


# Get a comment from Regulations.gov API 
async def get_comment_with_url(comment_id):
    regulations_api_key = settings.REGULATIONS_API_KEY
    async with httpx.AsyncClient() as client:
        comment_api = f"https://api.regulations.gov/v4/documents/{comment_id}?include=attachments&api_key={regulations_api_key}"
        response = await client.get(comment_api)
        return response
    
# Returns the list of all comment objects
def get_all_comments():
    # Fetch comment objects from database
    try:
        with open(database_path, 'r') as db:
            comments = json.load(db)
        
        # Check if the database is empty
        if len(comments) == 0:
            return response_data(status=204, data=None, message="No comment found.")
        
        # Return all retrieved comments
        else:
            return response_data(status=200, data=comments, message="Successful request.")
    
    # Handle error exceptions
    except FileNotFoundError:
        return response_data(status=500, data=None, message="Server Error: Database not found.")
    
    except json.JSONDecodeError:
        return response_data(status=500, data=None, message="Server Error: Failed to decode database file.")
    
    except PermissionError:
        return response_data(status=500, data=None, message="Server Error: Denied permission to access the database.")
    
    except Exception as e:
        return response_data(status=500, data=None, message="Unexpected server error occured: {e}")
        

# Returns an object of the comment
def get_comment(comment_id):
    response = get_all_comments()

    if response.status == 200:
        comments = response.data

        for comment in comments:
            if comment['data']['id'] == comment_id:
                return response_data(status=200, data=comment, message="Successful request.")
        
        # Comment not found
        return response_data(status=404, data=None, message=f"Comment {comment_id} not found.")
    
    else:
        raise Exception(response.status, response.message)
