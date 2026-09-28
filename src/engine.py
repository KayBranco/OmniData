"""
Orquestrador central do OmniData.
Recebe as solicitações e despacha para o agente especialista correspondente.
"""
from agents.sql_agent import SQLAgent
from agents.pbi_agent import PowerBIAgent
from agents.excel_agent import ExcelAgent

class OmniDataEngine:
    def __init__(self, user_role: str = "Engenheiro"):
        self.user_role = user_role
        
        # Instanciar os agentes especialistas
        self.sql_agent = SQLAgent()
        self.pbi_agent = PowerBIAgent()
        self.excel_agent = ExcelAgent()

    def process_request(self, domain: str, query: str):
        """Despacha a consulta para o agente especialista com base no domínio selecionado."""
        if domain == "sql":
            return self.sql_agent.generate_query(query)
        elif domain == "powerbi":
            return self.pbi_agent.get_dax_formula(query)
        elif domain == "excel":
            return self.excel_agent.generate_script(query)
        else:
            return {"erro": "Domínio técnico desconhecido."}