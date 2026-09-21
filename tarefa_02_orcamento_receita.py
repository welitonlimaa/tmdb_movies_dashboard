"""Tarefa 02 — relacao entre orcamento e receita.

Objetivo especifico:
Analisar a relacao entre orcamento e receita dos filmes.
Verificar se filmes com maiores investimentos apresentam maiores receitas.

Graficos desta tarefa (pode haver mais de um):
1. Grafico de dispersao. Eixo X = orcamento, eixo Y = receita.
   Cada ponto e um filme. Serve para ver se, no geral, gastar mais
   acompanha arrecadar mais.
2. Grafico de barras. Os 10 filmes de maior receita, com orcamento e
   receita lado a lado. Serve para enxergar casos extremos: filme caro
   que arrecadou pouco, ou filme mais barato que arrecadou muito.

A explicacao do resultado (o que o grafico permite concluir) deve ser
escrita como comentario no codigo, ao lado do grafico. Nao crie outro
arquivo so para esse texto.
"""

import streamlit as st
import pandas as pd

from preparacao import carregar_base, filmes_com_dinheiro, imprimir_colunas


def exibir(base: pd.DataFrame) -> None:
    """Mostra a secao desta tarefa no dashboard."""
    st.header("1. Orçamento e receita")
    st.write(
        "Pergunta: filmes com maior orçamento geram maior receita? "
        "Os gráficos desta seção usam apenas filmes lançados com os dois valores informados."
    )

    filmes = filmes_com_dinheiro(base)
    st.caption(f"{len(filmes)} filmes entram nesta comparação.")

    st.subheader("Dispersão: orçamento x receita")
    # Grafico 1 — dispersao.
    # Substitua o aviso abaixo por algo nesta linha:
    # st.scatter_chart(filmes, x="orcamento", y="receita")
    #
    # Explicacao (comentario obrigatorio, escrito depois de olhar o grafico):
    # Diga se a nuvem de pontos sobe junto com o orcamento ou se ha muitos
    # filmes caros com receita baixa e filmes baratos com receita alta.
    st.info("Gráfico de dispersão ainda não foi feito. Edite tarefa_02_orcamento_receita.py.")

    st.subheader("Barras: 10 maiores receitas")
    # Grafico 2 — barras agrupadas.
    # top = filmes.nlargest(10, "receita").set_index("titulo")[["orcamento", "receita"]]
    # st.bar_chart(top)
    #
    # Explicacao (comentario obrigatorio):
    # Diga se, entre esses 10, o maior orcamento e tambem a maior receita,
    # ou se a ordem dos gastos nao acompanha a ordem do arrecadado.
    st.info("Gráfico de barras ainda não foi feito. Edite tarefa_02_orcamento_receita.py.")


if __name__ == "__main__":
    # Rode este arquivo sozinho com:
    # python -m streamlit run tarefa_02_orcamento_receita.py
    # No terminal, python tarefa_02_orcamento_receita.py so imprime as colunas
    # se o Streamlit nao estiver conduzindo a pagina. Com streamlit run, a
    # pagina abre e as colunas tambem sao impressas uma vez.
    st.set_page_config(page_title="Tarefa 02 — Orçamento e receita", layout="wide")
    base = carregar_base()
    imprimir_colunas(base)
    exibir(base)
