from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_token_header

router = APIRouter(
    prefix = "/comments",          
    tags = ["comments"],
    responses = {404: {"description": "Not found"}}
)

fake_comments_db = [
    {"comment_id": "DROC-2342-3453-6544", "comment_title": "AI in the use of arts", "file_name": "DROC-2345-4435-4563", "file_size": 23, "word_count": 24252, "file_content": "A comment on usage of AI"},
    {"comment_id": "DROC-0000-0002-4443", "comment_title": "Miss use of AI", "file_name": "DROC-2345-4435-4563", "file_size": 23, "word_count": 24252, "file_content": "A comment on usage of AI"},
]

@router.get("/")
async def read_comments():
    return fake_comments_db

# @router.get("/{comment_id}")
# async def read_comment(comment_id: str):
#     for comment in fake_comments_db:
#         if(comment[comment_id] == )
#     return {"comment_id": comment_id}

