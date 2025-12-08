# llm_service.py
from app.core.config import settings
import google.generativeai as genai
import requests


# -------------------------------
# Gemini Client (v1 API)
# -------------------------------
def _ask_gemini(prompt):
    if not settings.LLM_API_KEY:
        raise ValueError("Gemini API key missing. Check LLM_API_KEY in .env")

    # Configure Gemini API key
    genai.configure(api_key=settings.LLM_API_KEY)

    # Use correct v1 constructor (avoid v1beta fallback)
    model = genai.GenerativeModel(model_name=settings.LLM_MODEL)

    # Generate response
    response = model.generate_content(prompt)

    # Extract Gemini text output
    return response.text


# -------------------------------
# Ollama Client (Local models)
# -------------------------------
def _ask_ollama(prompt):
    payload = {"model": settings.LLM_MODEL, "prompt": prompt}
    r = requests.post("http://localhost:11434/api/generate", json=payload)

    if r.status_code != 200:
        raise RuntimeError(f"Ollama Error {r.status_code}: {r.text}")

    return r.json().get("response")


# -------------------------------
# Hugging Face Inference API
# -------------------------------
def _ask_huggingface(prompt):
    if not settings.LLM_API_KEY:
        raise ValueError("HuggingFace API key missing. Check LLM_API_KEY in .env")

    API_URL = f"https://router.huggingface.co/hf-inference/models/{settings.LLM_MODEL}"
    headers = {"Authorization": f"Bearer {settings.LLM_API_KEY}"}
    payload = {"inputs": prompt}

    r = requests.post(API_URL, headers=headers, json=payload)

    if r.status_code != 200:
        raise RuntimeError(f"HuggingFace Error {r.status_code}: {r.text}")

    data = r.json()

    # HF TextGen models output:
    # [{"generated_text": "..."}]
    if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
        return data[0]["generated_text"]

    return str(data)



# -------------------------------
# Unified LLM Router
# -------------------------------
def ask_llm(prompt):
    provider = settings.LLM_PROVIDER.upper()

    if provider == "GEMINI":
        return _ask_gemini(prompt)

    if provider == "OLLAMA":
        return _ask_ollama(prompt)

    if provider == "HUGGINGFACE":
        return _ask_huggingface(prompt)

    raise ValueError(f"Unsupported LLM provider: {provider}")
