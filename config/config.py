from pydantic_settings import BaseSettings

# Setting up secret environment variables
class Settings(BaseSettings):
    APP_NAME: str = "Making Sense Of The Copyright Office Comments"
    REGULATIONS_API_KEY: str
    OPENAI_API_KEY: str
    LOCAL_DB_PATH: str
    CONFIG_PATH: str
    OUTPUT_PATH: str

settings = Settings()