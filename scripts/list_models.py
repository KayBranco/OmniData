import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Initialize client (uses GEMINI_API_KEY env var automatically)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def main():
    print("Listando modelos disponíveis e métodos suportados:\n")
    for m in client.models.list():
        methods = getattr(m, "supported_generation_methods", None) or []
        name = getattr(m, "name", getattr(m, "model", str(m)))
        print(f"{name} -> {methods}")

if __name__ == "__main__":
    main()
