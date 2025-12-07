from pymongo import MongoClient
from app.core.config import settings
from datetime import datetime

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]

documents_collection = db["documents"]
chunks_collection = db["chunks"]

def save_document(filename, s3_url):
    doc = {
        "filename": filename,
        "s3_url": s3_url,
        "status": "processing",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    result = documents_collection.insert_one(doc)
    return str(result.inserted_id)

def update_document(document_id, chunk_count):
    documents_collection.update_one(
        {"_id": document_id},
        {"$set": {"status": "processed", "chunk_count": chunk_count}}
    )
