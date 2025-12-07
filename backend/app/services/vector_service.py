import os
import chromadb
from chromadb.utils import embedding_functions
from app.services.mongo_service import save_chunk

# Chroma persistent storage
CHROMA_DIR = os.path.join(os.getcwd(), ".chromadb")
client = chromadb.PersistentClient(path=CHROMA_DIR)

# Chroma collection
collection = client.get_or_create_collection(
    name="rag_collection",
    metadata={"hnsw:space": "cosine"} 
)

# Local embedding model
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def store_embeddings(chunks, document_id):
    """
    - Saves chunk text into MongoDB (save_chunk)
    - Generates embeddings
    - Saves embeddings + chunk text + metadata into ChromaDB
    """
    if not chunks:
        raise ValueError("store_embeddings() received no chunks.")

    clean_chunks = [c.strip() for c in chunks if c.strip()]
    if not clean_chunks:
        raise ValueError("All chunks are empty after cleaning.")

    # 1️⃣ SAVE CHUNKS TO MONGO
    for i, chunk in enumerate(clean_chunks):
        save_chunk(document_id, i, chunk)

    # 2️⃣ PREPARE IDs FOR CHROMA
    ids = [f"{document_id}_{i}" for i in range(len(clean_chunks))]

    # 3️⃣ GENERATE EMBEDDINGS
    embeddings = embed_fn(clean_chunks)
    if embeddings is None or len(embeddings) != len(clean_chunks):
        raise ValueError("Embedding generation failed.")

    # 4️⃣ STORE INTO CHROMADB
    collection.add(
        ids=ids,
        documents=clean_chunks,
        embeddings=embeddings,
        metadatas=[{"document_id": document_id} for _ in clean_chunks]
    )

    return len(clean_chunks)


def get_similar_chunks(query, top_k=4):
    """
    Returns the top-k most similar chunk texts for a query.
    """
    if not query or not query.strip():
        return []

    query_embedding = embed_fn([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    if "documents" not in results or not results["documents"]:
        return []

    return results["documents"][0]
