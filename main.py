from fastapi import FastAPI

from routers import comments
from config.config import settings

app = FastAPI()

app.include_router(comments.router)

@app.get("/")
async def root():
    return {"message": f"Welcome {settings.APP_NAME}"}
