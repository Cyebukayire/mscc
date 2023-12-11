from fastapi import FastAPI

from routers import comments

app = FastAPI()

app.include_router(comments.router)

@app.get("/")
async def root():
    return {"message": "Welcome\n Making Sense Of The Copyright Office Comments"}