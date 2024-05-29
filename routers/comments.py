from fastapi import APIRouter, HTTPException
from controllers.comments_external_api_controller import get_comment_metadata

router = APIRouter(
    prefix = "/comments",          
    tags = ["comments"],
    responses = {404: {"description": "Not found"}}
)

# Retrieve metadata of a single comment
@router.get("/{comment_id}") 
async def get_comment(comment_id: str):
    simple_metadata = await get_comment_metadata(comment_id)
    return simple_metadata
