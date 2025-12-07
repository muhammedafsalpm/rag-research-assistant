import os
from dotenv import load_dotenv
load_dotenv()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Mongo
    MONGO_URI: str
    MONGO_DB: str

    # AWS
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_BUCKET_NAME: str

    # LLM settings (REQUIRED)
    LLM_PROVIDER: str
    LLM_MODEL: str
    LLM_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
