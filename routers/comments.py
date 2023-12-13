from fastapi import APIRouter, HTTPException
from services.comments import fetch_comment
from utils.word_counter import word_counter

router = APIRouter(
    prefix = "/comments",          
    tags = ["comments"],
    responses = {404: {"description": "Not found"}}
)

# Retrieve metadata of a single comment
@router.get("/{comment_id}") 
async def read_comment(comment_id: str):
    response = await fetch_comment(comment_id)
    response_data = response.json()

    # Extra metadata
    if response.status_code == 200:
        comment_attributes = response_data['data']['attributes']
        
        # Check if the comment has an attachement and extract all simple metadata (EX: comment_id = 'COLC-2023-0006-0036')
        if 'included'in response_data:
            file_attributes = response_data['included'][0]['attributes']
            word_count = word_counter(file_attributes['fileFormats'][0]['fileUrl'])
            simple_metadata = {
                "comment_id": comment_id,
                "comment_title": comment_attributes['title'], 
                "file_name": file_attributes['title'], # URL =  file_attributes['fileFormats'][0]['fileUrl'], 
                "file_size": file_attributes['fileFormats'][0]['size'],
                "word_count": word_count
            }
            return simple_metadata
        
        # If comment has no attachement, extract few metadata (Ex: comment_id = 'COLC-2023-0006-0862')
        else:
            file_attributes = []
            word_count = word_counter(comment_attributes['comment'])
            simple_metadata = {
                "comment_id": comment_id,
                "comment_title": comment_attributes['title'], 
                "word_count": word_count
            }
            return simple_metadata
    else:
        raise HTTPException(status = response.status_code, message = "failed to fetch comment")
