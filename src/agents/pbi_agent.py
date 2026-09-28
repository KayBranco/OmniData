import os
from dotenv import load_dotenv
from google import genai
from .genai_utils import generate_with_retry, logger

load_dotenv()

# Initialize client (uses GEMINI_API_KEY env var automatically)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def _extract_text_from_response(response) -> str:
    try:
        return response.output[0].content[0].text
    except Exception:
        try:
            return getattr(response, "text", str(response))
        except Exception:
            return str(response)


class PowerBIAgent:
    def __init__(self):
        self.model_name = os.getenv("GEMINI_MODEL") or "gemini-2.5-flash"

    def get_dax_formula(self, metric_description: str) -> dict:
        prompt = f"""
        Você é um arquiteto especialista em Power BI e modelagem de dados corporativos (DAX).
        Crie uma fórmula DAX otimizada, limpa e profissional para atender à seguinte necessidade:
        Necessidade: {metric_description}

        Retorne a fórmula formatada de maneira clara.
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
            dax_result = _extract_text_from_response(response).replace("```dax", "").replace("```", "").strip()
        except Exception as e:
            logger.exception("Failed to generate DAX formula")
            dax_result = f"// Erro ao comunicar com a API do Gemini: {str(e)}"

        return {
            "dominio": "Power BI / DAX",
            "solicitacao": metric_description,
            "resultado_gerado": dax_result,
            "status": "Gerado dinamicamente via Gemini",
        }