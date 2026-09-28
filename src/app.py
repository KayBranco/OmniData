import streamlit as st
from engine import OmniDataEngine

# Configuração da página com layout largo e tema corporativo limpo
st.set_page_config(
    page_title="OmniData | Enterprise AI Suite",
    page_icon="O",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada para um aspeto moderno e profissional
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; color: #1E3A8A; font-weight: 700; margin-bottom: 0rem; }
    .sub-header { font-size: 1.1rem; color: #64748B; margin-bottom: 2rem; }
    .stButton>button { width: 100%; border-radius: 6px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# Inicializar o motor do OmniData (otimizado com cache para performance)
@st.cache_resource
def load_engine():
    return OmniDataEngine(user_role="Engenheiro")

engine = load_engine()

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown("### OmniData Suite")
    st.caption("Plataforma de IA Multidomínio Corporativa")
    st.markdown("---")
    
    perfil = st.selectbox("Perfil Ativo", ["Engenheiro de Processos", "Analista de Dados", "Gestor Técnico"])
    st.markdown("---")
    
    st.info(f"Utilizador: **{perfil}**\n\nSegurança: **RBAC Ativo**")
    st.markdown("---")
    st.markdown("**Versão:** 1.0.0-beta")

# --- CABEÇALHO PRINCIPAL ---
st.markdown('<p class="main-header">OmniData Copilot</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Acelere o desenvolvimento de consultas SQL, relatórios Power BI e automações com inteligência validada por schemas.</p>', unsafe_allow_html=True)

# --- ABAS SUPERIORES ---
tab1, tab2, tab3 = st.tabs([
    "Consultor SQL", 
    "Power BI (DAX)", 
    "Excel & Python"
])

# 1. ABA DO AGENTE SQL
with tab1:
    st.subheader("Consultor SQL Inteligente (Baseado em Schema)")
    st.write("Converta linguagem natural em código SQL estruturado, evitando alucinações através da leitura de schemas reais.")
    
    col_sql_1, col_sql_2 = st.columns([2, 1])
    
    with col_sql_1:
        pergunta_sql = st.text_area(
            "Descreva o que quer consultar:", 
            placeholder="Ex: Liste o tempo total de paradas por linha de produção",
            height=100
        )
        if st.button("Gerar Código SQL", type="primary", key="btn_sql"):
            if pergunta_sql:
                with st.spinner("A analisar schema e a traduzir para SQL..."):
                    resposta = engine.process_request("sql", pergunta_sql)
                st.success("Consulta gerada com sucesso!")
                st.code(resposta.get("sql_gerado"), language="sql")
                
                with st.expander("Ver Dicionário de Schemas Utilizado"):
                    st.json(resposta.get("schema_utilizado"))
            else:
                st.warning("Por favor, introduza uma descrição para a consulta.")
                
    with col_sql_2:
        st.markdown("### Dicas de Uso")
        st.info(
            "O agente cruza automaticamente tabelas corporativas como:\n"
            "- `linhas_producao`\n"
            "- `paradas_maquinas`\n"
            "- `apontamentos_qualidade`"
        )

# 2. ABA DO AGENTE POWER BI
with tab2:
    st.subheader("Especialista em Power BI & DAX")
    st.write("Obtenha fórmulas DAX complexas e métricas validadas pelo dicionário semântico oficial.")
    
    col_pbi_1, col_pbi_2 = st.columns([2, 1])
    
    with col_pbi_1:
        pergunta_pbi = st.text_input(
            "Qual métrica ou indicador precisa de calcular?", 
            placeholder="Ex: Como calcular o acumulado do ano (YTD) de refugo?"
        )
        if st.button("Gerar Fórmula DAX", type="primary", key="btn_pbi"):
            if pergunta_pbi:
                with st.spinner("A consultar regras de negócio e a estruturar DAX..."):
                    resposta = engine.process_request("powerbi", pergunta_pbi)
                st.success("Fórmula DAX gerada com sucesso:")
                st.code(resposta.get("resultado_gerado"), language="dax")
            else:
                st.warning("Por favor, descreva a métrica pretendida.")
                
    with col_pbi_2:
        st.markdown("### Padrões Suportados")
        st.info("Ideal para cálculos temporais complexos (`YTD`, `MTD`, acumulados móveis) e indicadores de eficiência de fábrica.")

# 3. ABA DO AGENTE EXCEL & PYTHON
with tab3:
    st.subheader("Automação de Dados (Excel, Python & VBA)")
    st.write("Crie scripts automáticos para tratamento de dados tabulares e limpeza de planilhas operacionais.")
    
    col_ex_1, col_ex_2 = st.columns([2, 1])
    
    with col_ex_1:
        pergunta_excel = st.text_input(
            "Descreva a automação necessária:", 
            placeholder="Ex: Limpar linhas vazias e calcular média móvel de 7 dias."
        )
        if st.button("Gerar Script de Automação", type="primary", key="btn_excel"):
            if pergunta_excel:
                with st.spinner("A gerar script otimizado em Python/Pandas..."):
                    resposta = engine.process_request("excel", pergunta_excel)
                st.success("Script gerado com sucesso:")
                st.code(resposta.get("resultado_gerado"), language="python")
            else:
                st.warning("Por favor, descreva a necessidade de automação.")
                
    with col_ex_2:
        st.markdown("### Produtividade")
        st.info("Gera códigos limpos utilizando bibliotecas padrão de mercado como **Pandas** prontos a aplicar nas planilhas do dia a dia.")