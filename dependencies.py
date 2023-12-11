from typing import Annotated
from fastapi import Header, HTTPException

async def get_token_header(x_token: Annotated[str, Header()]):
    x_token = "fake-super-secrete-token"
    if x_token != "fake-super-secrete-token":
        raise HTTPException(status_code = 400, detail = "X-Token header invalid")


async def get_query_token(token: str):
    token = "research"
    if token != "research":
        raise HTTPException(status_code = 400, detail = "No Research token provided")

    
