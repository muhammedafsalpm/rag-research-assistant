from app.utils.pdf_utils import extract_text_from_pdf
from app.utils.chunk_utils import chunk_text
from app.services.vector_service import store_embeddings

def process_document(path, document_id):
    text = extract_text_from_pdf(path)
    chunks = chunk_text(text)
    count = store_embeddings(chunks, document_id)
    return count
