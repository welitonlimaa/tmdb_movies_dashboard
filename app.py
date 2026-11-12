"""Dashboard final. Junta as tres tarefas em uma unica pagina.
"""

import importlib

import streamlit as st

import preparacao
import tarefa_02_orcamento_receita as tarefa_02
import tarefa_03_generos as tarefa_03
import tarefa_04_avaliacao_popularidade as tarefa_04


importlib.reload(preparacao)
importlib.reload(tarefa_02)
importlib.reload(tarefa_03)
importlib.reload(tarefa_04)

carregar_base = preparacao.carregar_base
descricao_colunas = preparacao.descricao_colunas
filmes_com_dinheiro = preparacao.filmes_com_dinheiro
filmes_para_avaliacao = preparacao.filmes_para_avaliacao
imprimir_colunas = preparacao.imprimir_colunas
exibir_orcamento_receita = tarefa_02.exibir
exibir_generos = tarefa_03.exibir
exibir_avaliacao = tarefa_04.exibir

st.set_page_config(page_title="Desempenho de filmes", layout="wide")

st.markdown(
    """
    <style>
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        .block-container {
            max-width: 100% !important;
        }
        .block-container {
            padding-top: 1.35rem;
            padding-bottom: 1.6rem;
            padding-left: 2px !important;
            padding-right: 2px !important;
        }
        [data-testid="stHeader"] {
            background: transparent;
        }
        .dash-head h1 {
            margin: 0;
            font-size: 1.55rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            line-height: 1.15;
            text-align: left;
        }
        .dash-sub {
            margin: 0.28rem 0 0;
            font-size: 0.82rem;
            opacity: 0.62;
            line-height: 1.35;
        }
        h2 {
            font-size: 0.98rem !important;
            font-weight: 700 !important;
            margin-top: 1.15rem !important;
            margin-bottom: 0 !important;
        }
        h3 {
            font-size: 0.92rem !important;
            font-weight: 650 !important;
            margin-bottom: 0.15rem !important;
        }
        div[data-testid="stCaptionContainer"] {
            margin-top: 0.1rem;
            margin-bottom: 0.35rem;
        }
        .st-key-painel_tema_1,
        .st-key-painel_tema_2,
        .st-key-painel_tema_3 {
            border-radius: 16px !important;
            padding: 0.35rem 0.3rem 0.9rem !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        [class*="st-key-card_"] {
            border-radius: 16px !important;
            background: light-dark(#ffffff, #232838) !important;
            border: 1px solid light-dark(#e6eaf2, #343b52) !important;
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.16) !important;
            padding: 0.85rem 1rem 0.75rem !important;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.85rem;
            font-weight: 700;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 0.84rem;
            font-weight: 600;
        }
        .st-key-kpi_filmes,
        .st-key-kpi_dinheiro,
        .st-key-kpi_nota {
            border: none !important;
            border-radius: 16px !important;
            box-shadow: 0 10px 24px rgba(20, 24, 40, 0.22) !important;
            padding: 0.85rem 1rem 0.7rem !important;
        }
        .st-key-kpi_filmes {
            background: linear-gradient(135deg, #5b8cff 0%, #3d62e0 100%) !important;
        }
        .st-key-kpi_dinheiro {
            background: linear-gradient(135deg, #8b6cf6 0%, #6d4adf 100%) !important;
        }
        .st-key-kpi_nota {
            background: linear-gradient(135deg, #f5a24a 0%, #ef7d2a 100%) !important;
        }
        .st-key-kpi_filmes [data-testid="stMetricLabel"],
        .st-key-kpi_filmes [data-testid="stMetricLabel"] *,
        .st-key-kpi_filmes [data-testid="stMetricValue"],
        .st-key-kpi_dinheiro [data-testid="stMetricLabel"],
        .st-key-kpi_dinheiro [data-testid="stMetricLabel"] *,
        .st-key-kpi_dinheiro [data-testid="stMetricValue"],
        .st-key-kpi_nota [data-testid="stMetricLabel"],
        .st-key-kpi_nota [data-testid="stMetricLabel"] *,
        .st-key-kpi_nota [data-testid="stMetricValue"] {
            color: #ffffff !important;
        }
    </style>
    <div class="dash-head">
        <h1>Análise do desempenho de filmes</h1>
        <p class="dash-sub">Grupo 6 — Darlan José de Oliveira, Weliton Pereira Lima Junior, Jonathas dos Santos Fideles, Silvana dos Santos Vieira, Alexander Nascimento Santos e Richardson da Silva Freitas.</p>
        <p class="dash-sub">Gênero, orçamento, receita, popularidade e avaliação do público.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

base = carregar_base()
if "colunas_impressas" not in st.session_state:
    imprimir_colunas(base)
    st.session_state["colunas_impressas"] = True

com_dinheiro = filmes_com_dinheiro(base)
com_nota = filmes_para_avaliacao(base)
nota_geral = com_nota["nota_media"].mean()

coluna_filmes, coluna_dinheiro, coluna_nota = st.columns(3, gap="medium", wrap=False)
with coluna_filmes:
    with st.container(border=True, key="kpi_filmes"):
        st.metric("Filmes na base", f"{len(base)}")
with coluna_dinheiro:
    with st.container(border=True, key="kpi_dinheiro"):
        st.metric("Com orçamento e receita", f"{len(com_dinheiro)}")
with coluna_nota:
    with st.container(border=True, key="kpi_nota"):
        st.metric("Nota média (50 votos ou mais)", f"{nota_geral:.1f}")

coluna_tema_1, coluna_tema_3 = st.columns(2, gap="medium", wrap=False)
with coluna_tema_1:
    with st.container(border=True, key="painel_tema_1"):
        exibir_orcamento_receita(base)
with coluna_tema_3:
    with st.container(border=True, key="painel_tema_3"):
        exibir_avaliacao(base)

with st.container(border=True, key="painel_tema_2"):
    exibir_generos(base)

with st.expander("Colunas da base (labels)"):
    st.write(
        "Estes são os nomes usados no código. A coluna original é o nome "
        "que veio no CSV, antes da limpeza."
    )
    st.dataframe(descricao_colunas(base), hide_index=True, width="stretch")
