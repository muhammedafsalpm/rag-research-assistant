import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # AWS
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB")

    # LLM
    LLM_PROVIDER = os.getenv("LLM_PROVIDER")
    LLM_MODEL = os.getenv("LLM_MODEL")
    LLM_API_KEY = os.getenv("LLM_API_KEY")

settings = Settings()
