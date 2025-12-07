import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings

client = chromadb.Client()
collection = client.get_or_create_collection(
    name="rag_collection"
)

# Local free embeddings
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def store_embeddings(chunks, document_id):
    ids = []
    for i, chunk in enumerate(chunks):
        ids.append(f"{document_id}_{i}")

    embeddings = embed_fn(chunks)

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"document_id": document_id} for _ in chunks]
    )

    return len(ids)


def get_similar_chunks(query, top_k=4):
    query_embedding = embed_fn([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results["documents"][0]
