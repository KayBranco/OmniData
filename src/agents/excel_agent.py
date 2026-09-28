import os
from dotenv import load_dotenv
from google import genai
from .genai_utils import generate_with_retry, logger

load_dotenv()

# Initialize client (uses GEMINI_API_KEY env var automatically)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def _extract_text_from_response(response) -> str:
    # Support multiple response shapes returned by different SDK versions
    try:
        # Newer genai responses may have nested output/content text
        return response.output[0].content[0].text
    except Exception:
        try:
            return getattr(response, "text", str(response))
        except Exception:
            return str(response)


class ExcelAgent:
    def __init__(self):
        self.model_name = os.getenv("GEMINI_MODEL") or "gemini-2.5-flash"

    def generate_script(self, prompt_text: str) -> dict:
        prompt = f"""
        Você é um engenheiro especialista em automação de dados utilizando Python (Pandas) e Excel.
        Escreva um script em Python robusto, comentado e limpo para resolver o seguinte problema operacional:
        Solicitação: {prompt_text}

        Retorne apenas o código Python estruturado.
        """

        try:
            model_candidates = [
                self.model_name,
                "models/gemini-2.5-flash",
                "models/gemini-3.5-flash-lite",
                "models/gemini-3.5-flash",
            ]
            response = generate_with_retry(
                client,
                model_candidates,
                contents=[prompt],
            )
            script_result = _extract_text_from_response(response).replace("```python", "").replace("```", "").strip()
        except Exception as e:
            logger.exception("Failed to generate script")
            script_result = f"# Erro ao comunicar com a API do Gemini: {str(e)}"

        return {
            "dominio": "Excel e Automacao (Python/VBA)",
            "solicitacao": prompt_text,
            "resultado_gerado": script_result,
            "status": "Gerado dinamicamente via Gemini",
        }