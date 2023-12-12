from pydantic_settings import BaseSettings

# Setting up secret environment variables
class Settings(BaseSettings):
    APP_NAME: str = "Making Sense Of The Copyright Office Comments"
    API_KEY: str

settings = Settings()