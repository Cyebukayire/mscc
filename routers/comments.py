from fastapi import APIRouter
from controllers.comments_external_api_controller import get_comment_metadata
from controllers.comments_local_db_controller import get_all_metadata, update_comment_entity, get_cited_case_laws, count_cited_case_laws

router = APIRouter(
    prefix = "/comments",          
    tags = ["comments"],
    responses = {404: {"description": "Not found"}}
)

# Retrieve metadata of all comments
@router.get("/all") 
async def get_comment():
    all_metadata = await get_all_metadata()
    return all_metadata

# Get cited case laws
@router.get("/citations/all")
def get_citations():
    citations = get_cited_case_laws()
    return citations

@router.get("/citations/rank")
def get_citations():
    analysis = count_cited_case_laws()
    return analysis

# Retrieve metadata of a single comment
@router.get("/{comment_id}") 
async def get_comment(comment_id: str):
    simple_metadata = await get_comment_metadata(comment_id)
    return simple_metadata

# Update Entity
@router.put("/entity")
def update_entity():
    message = update_comment_entity()
    return message

