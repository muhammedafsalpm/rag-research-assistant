def chunk_text(text, chunk_size=500, overlap=50):
    if not text or not text.strip():
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:  # avoid empty chunks
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks
