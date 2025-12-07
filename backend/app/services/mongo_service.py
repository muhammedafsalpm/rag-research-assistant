from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from app.core.config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]
documents = db.documents
chunks_collection = db.chunks



def save_document(filename, s3_url):
    doc = {
        "filename": filename,
        "s3_url": s3_url,
        "status": "processing",
        "chunk_count": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = documents.insert_one(doc)
    return str(result.inserted_id)

def save_chunk(document_id, index, text):
    chunk_doc = {
        "document_id": document_id,
        "index": index,
        "text": text,
        "created_at": datetime.utcnow()
    }
    chunks_collection.insert_one(chunk_doc)


def update_document(document_id, chunk_count):
    documents.update_one(
        {"_id": ObjectId(document_id)},
        {
            "$set": {
                "chunk_count": chunk_count,
                "status": "ready",
                "updated_at": datetime.utcnow()
            }
        }
    )
