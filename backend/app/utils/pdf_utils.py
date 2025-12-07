import pdfplumber

def extract_text_from_pdf(pdf_source, is_bytes=False):
    if is_bytes:
        with pdfplumber.open(pdf_source) as pdf:
            text = ""
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text

    # old path mode
    with pdfplumber.open(pdf_source) as pdf:
        text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text

