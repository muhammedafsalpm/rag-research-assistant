from app.core.config import settings

# -------------------------------
# Gemini Client
# -------------------------------
import google.generativeai as genai

def _ask_gemini(prompt):
    genai.configure(api_key=settings.LLM_API_KEY)
    model = genai.GenerativeModel(settings.LLM_MODEL)
    response = model.generate_content(prompt)
    return response.text


# -------------------------------
# Ollama Client (future local use)
# -------------------------------
import requests

def _ask_ollama(prompt):
    payload = {"model": settings.LLM_MODEL, "prompt": prompt}
    r = requests.post("http://localhost:11434/api/generate", json=payload)
    return r.json().get("response")


# -------------------------------
# Router — The main function you call
# -------------------------------
def ask_llm(prompt):
    provider = settings.LLM_PROVIDER.upper()

    if provider == "GEMINI":
        return _ask_gemini(prompt)

    if provider == "OLLAMA":
        return _ask_ollama(prompt)

    raise ValueError(f"Unsupported LLM provider: {provider}")
