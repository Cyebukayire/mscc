from fastapi import APIRouter, HTTPException
from services.comments import fetch_comment

router = APIRouter(
    prefix = "/comments",          
    tags = ["comments"],
    responses = {404: {"description": "Not found"}}
)

# Retrieve metadata of a single comment
@router.get("/{comment_id}") # EX: comment_id = 'COLC-2023-0006-0036'
async def read_comment(comment_id: str):
    response = await fetch_comment(comment_id)
    response_data = response.json()

    # Extra metadata
    if response.status_code == 200:
        comment_attributes = response_data['data']['attributes']
        
        # Check if the comment has an attachement 
        if 'included'in response_data:
            file_attributes = response_data['included'][0]['attributes']
            simple_metadata = {
                "comment_id": comment_id,
                "comment_title": comment_attributes['title'], # ?? file title (though some comments don't have file)
                "file_name": file_attributes['fileFormats'][0]['fileUrl'], # TODO: Extract file name
                "file_size": file_attributes['fileFormats'][0]['size'],
                "file_title": file_attributes['title'],
                "word_count": 0 # TODO: To be calculated manually
            }
            return simple_metadata
        
        # If comment has no attachement, extract few metadata
        else:
            file_attributes = []
            simple_metadata = {
                "comment_id": comment_id,
                "comment_title": comment_attributes['title'], # ?? file title (though some comments don't have file)
                "word_count": 0 # TODO: To be calculated manually
            }
            return simple_metadata
    else:
        raise HTTPException(status = response.status_code, message = "failed to fetch comment")
