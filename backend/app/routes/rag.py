from fastapi import APIRouter, UploadFile, File
import uuid
import os

from app.services.s3_service import upload_to_s3
from app.services.mongo_service import save_document, update_document
from app.services.rag_pipeline import process_document
from app.services.vector_service import get_similar_chunks
from app.services.llm_service import ask_llm

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    local_path = os.path.join(os.getcwd(), f"{file_id}.pdf")

    with open(local_path, "wb") as f:
        f.write(await file.read())

    # upload to S3
    s3_key = f"documents/{file_id}.pdf"
    s3_url = upload_to_s3(local_path, s3_key)

    # save metadata
    document_id = save_document(file.filename, s3_url)

    # process RAG
    chunk_count = process_document(local_path, document_id)

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
