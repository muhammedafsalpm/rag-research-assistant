from fastapi import FastAPI
from app.routes.rag import router as rag_router

app = FastAPI()

app.include_router(rag_router, prefix="/api/v1")
