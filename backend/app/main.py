# main.py
import os
from dotenv import load_dotenv

# Make sure .env loads BEFORE importing config or other modules
load_dotenv()

from fastapi import FastAPI
from app.routes.rag import router as rag_router

app = FastAPI()

app.include_router(rag_router, prefix="/api/v1")
