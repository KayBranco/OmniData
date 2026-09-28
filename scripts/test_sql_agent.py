import os
import sys
from dotenv import load_dotenv

# ensure project root is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

from src.agents.sql_agent import SQLAgent

def main():
    agent = SQLAgent()
    q = "Quantas paradas de máquinas tiveram duração maior que 60 minutos na última semana?"
    result = agent.generate_query(q)
    print('Pergunta:', result['pergunta_usuario'])
    print('SQL gerado:\n', result['sql_gerado'])

if __name__ == '__main__':
    main()
