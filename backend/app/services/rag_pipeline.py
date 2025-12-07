from app.utils.pdf_utils import extract_text_from_pdf
from app.utils.chunk_utils import chunk_text
from app.services.vector_service import store_embeddings

from io import BytesIO
import pdfplumber

def process_document(pdf_data, document_id, is_bytes=False):
    # Read PDF from bytes
    if is_bytes:
        pdf_file = BytesIO(pdf_data)
    else:
        pdf_file = pdf_data  # old behavior

    text = extract_text_from_pdf(pdf_file, is_bytes=True)
    chunks = chunk_text(text)
    return store_embeddings(chunks, document_id)