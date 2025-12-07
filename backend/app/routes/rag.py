from fastapi import APIRouter, UploadFile, File
import uuid
import os

from app.services.s3_service import upload_to_s3
from app.services.mongo_service import (
    save_document,
    update_document,
    chunks_collection 
)
from app.services.rag_pipeline import process_document
from app.services.vector_service import get_similar_chunks
from app.services.llm_service import ask_llm

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise ValueError("Only PDF files are accepted.")

    file_id = str(uuid.uuid4())

    # Read file bytes (avoid local file)
    file_bytes = await file.read()

    # Upload to S3 directly
    s3_key = f"documents/{file_id}.pdf"
    s3_url = upload_to_s3(file_bytes, s3_key, is_bytes=True)

    # Save base metadata in MongoDB
    document_id = save_document(file.filename, s3_url)

    # Process PDF from bytes
    chunk_count = process_document(file_bytes, document_id, is_bytes=True)

    # Update Mongo with chunk count and status
    update_document(document_id, chunk_count)

    return {"document_id": document_id, "chunks": chunk_count}


@router.post("/query")
async def query_rag(query: dict):
    question = query["question"]

    chunks = get_similar_chunks(question)
    context = "\n\n".join(chunks)

    prompt = f"""
    Use the following context to answer the question.

    Context:
    {context}

    Question:
    {question}

    Answer based only on the context:
    """

    answer = ask_llm(prompt)
    return {"answer": answer}


@router.get("/chunks/{document_id}")
def get_chunks(document_id: str):
    items = chunks_collection.find({"document_id": document_id})
    return [{"index": item["index"], "text": item["text"]} for item in items]
