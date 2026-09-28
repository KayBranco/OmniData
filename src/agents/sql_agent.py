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


class SQLAgent:
    def __init__(self):
        self.database_schema = {
            "linhas_producao": ["id", "linha_nome", "setor", "capacidade_nominal"],
            "paradas_maquinas": ["id", "linha_id", "motivo_parada", "duracao_minutos", "data_registro"],
            "apontamentos_qualidade": ["id", "peca_id", "status_aprovacao", "motivo_refugo", "turno"],
        }
        self.model_name = os.getenv("GEMINI_MODEL") or "gemini-2.5-flash"

    def generate_query(self, natural_language_query: str) -> dict:
        schema_str = str(self.database_schema)
        prompt = f"""
        Você é um Engenheiro de Dados e especialista em SQL sênior. 
        Baseie-se estritamente no schema do banco de dados abaixo para evitar alucinações. Não invente tabelas ou colunas.
        Schema disponível: {schema_str}

        Converta a seguinte pergunta do usuário em uma consulta SQL limpa e executável:
        Pergunta: {natural_language_query}

        Retorne apenas o código SQL de forma limpa, sem blocos de markdown adicionais se possível.
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
            sql_result = _extract_text_from_response(response).replace("```sql", "").replace("```", "").strip()
        except Exception as e:
            logger.exception("Failed to generate SQL")
            sql_result = f"-- Erro ao comunicar com a API do Gemini: {str(e)}"

        return {
            "dominio": "SQL (Consultador Baseado no TG)",
            "pergunta_usuario": natural_language_query,
            "schema_utilizado": self.database_schema,
            "sql_gerado": sql_result,
            "status": "Sucesso - Gerado dinamicamente via Gemini",
        }