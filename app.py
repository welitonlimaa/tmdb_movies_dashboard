"""Dashboard final. Junta as tres tarefas em uma unica pagina.

Rode na pasta do projeto:
python -m streamlit run app.py
"""

import importlib

import streamlit as st

import preparacao
import tarefa_01_orcamento_receita as tarefa_01
import tarefa_02_generos as tarefa_02
import tarefa_03_avaliacao_popularidade as tarefa_03

# Sem este reload, o Streamlit continua com a versao antiga do arquivo
# importado e a pessoa nao ve o grafico que acabou de salvar.
importlib.reload(preparacao)
importlib.reload(tarefa_01)
importlib.reload(tarefa_02)
importlib.reload(tarefa_03)

carregar_base = preparacao.carregar_base
descricao_colunas = preparacao.descricao_colunas
filmes_com_dinheiro = preparacao.filmes_com_dinheiro
filmes_para_avaliacao = preparacao.filmes_para_avaliacao
imprimir_colunas = preparacao.imprimir_colunas
exibir_orcamento_receita = tarefa_01.exibir
exibir_generos = tarefa_02.exibir
exibir_avaliacao = tarefa_03.exibir

st.set_page_config(page_title="Desempenho de filmes", layout="wide")

st.title("Análise do desempenho de filmes")
st.caption(
    "Grupo 6 — Darlan José de Oliveira, Weliton Pereira Lima Junior, "
    "Jonathas dos Santos Fideles, Silvana dos Santos Vieira, "
    "Alexander Nascimento Santos e Richardson da Silva Freitas."
)
st.write(
    "Este dashboard organiza dados públicos de filmes para relacionar "
    "gênero, orçamento, receita, popularidade e avaliação do público."
)

base = carregar_base()
if "colunas_impressas" not in st.session_state:
    imprimir_colunas(base)
    st.session_state["colunas_impressas"] = True

with st.expander("Colunas da base (labels)"):
    st.write(
        "Estes são os nomes usados no código. A coluna original é o nome "
        "que veio no CSV, antes da limpeza."
    )
    st.dataframe(descricao_colunas(base), hide_index=True, width="stretch")

# Cartoes (KPI): um dos tipos de visualizacao pedidos na etapa 2.
# Eles resumem o tamanho da base. Nao substituem os graficos das tarefas.
com_dinheiro = filmes_com_dinheiro(base)
com_nota = filmes_para_avaliacao(base)
nota_geral = com_nota["nota_media"].mean()

st.subheader("Visão geral")
coluna_filmes, coluna_dinheiro, coluna_nota = st.columns(3)
coluna_filmes.metric("Filmes na base", f"{len(base)}")
coluna_dinheiro.metric("Com orçamento e receita", f"{len(com_dinheiro)}")
coluna_nota.metric("Nota média (50 votos ou mais)", f"{nota_geral:.1f}")

st.divider()
exibir_orcamento_receita(base)
st.divider()
exibir_generos(base)
st.divider()
exibir_avaliacao(base)

st.divider()
st.caption(
    "A explicação de cada gráfico fica como comentário no arquivo da tarefa "
    "(tarefa_01_orcamento_receita.py, tarefa_02_generos.py e "
    "tarefa_03_avaliacao_popularidade.py)."
)
