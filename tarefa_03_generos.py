"""Tarefa 02 — generos com maior popularidade e receita.

Objetivo especifico:
Identificar os generos com maior popularidade e receita.
Comparar o desempenho dos diferentes generos de filmes.

Graficos desta tarefa (pode haver mais de um):
1. Grafico de barras da receita media por genero.
   Responde quais generos arrecadam mais, em media, por filme.
2. Grafico de barras da popularidade media por genero.
   Responde quais generos sao mais populares.
3. Grafico de pizza, somente se ficar restrito a poucos generos
   (por exemplo, os 5 de maior receita media). Com todos os generos
   a pizza fica impossivel de ler. As barras sao a escolha principal.

Atencao: um filme pode ter varios generos. Somar a receita conta o
mesmo dinheiro mais de uma vez. resumo_por_genero ja calcula a media.

A explicacao do resultado deve ser escrita como comentario no codigo,
ao lado de cada grafico. Nao crie outro arquivo so para esse texto.
"""

import streamlit as st
import pandas as pd

from preparacao import carregar_base, imprimir_colunas, resumo_por_genero


def exibir(base: pd.DataFrame) -> None:
    """Mostra a secao desta tarefa no dashboard."""
    st.header("2. Gêneros, popularidade e receita")
    st.write(
        "Pergunta: quais gêneros apresentam maior popularidade e receita? "
        "Os números são médias por filme lançado, para não contar duas vezes "
        "quem tem mais de um gênero."
    )

    resumo = resumo_por_genero(base)
    st.caption(f"{len(resumo)} gêneros na base.")

    st.subheader("Barras: receita média por gênero")
    # Grafico 1 — barras.
    # st.bar_chart(resumo.set_index("genero")[["receita_media"]])
    #
    # Explicacao (comentario obrigatorio):
    # Cite os generos do topo e diga se a lideranca e folgada ou se varios
    # generos ficam proximos.
    st.info("Gráfico de receita por gênero ainda não foi feito. Edite tarefa_02_generos.py.")

    st.subheader("Barras: popularidade média por gênero")
    # Grafico 2 — barras.
    # st.bar_chart(resumo.set_index("genero")[["popularidade_media"]])
    #
    # Explicacao (comentario obrigatorio):
    # Diga se os generos mais populares sao os mesmos da maior receita media.
    st.info("Gráfico de popularidade por gênero ainda não foi feito. Edite tarefa_02_generos.py.")

    st.subheader("Pizza opcional: participação dos 5 gêneros de maior receita")
    # Grafico 3 — pizza, so com o topo. Streamlit nao tem st.pie_chart pronto.
    # Da para usar o pandas para ficar nos 5 primeiros e, se quiserem pizza,
    # instalar uma biblioteca extra. Se o grupo preferir, este grafico pode
    # ser mais um de barras. Nao e obrigatorio.
    #
    # Explicacao (comentario obrigatorio, se o grafico for feito):
    # Diga quanto do conjunto esses 5 generos representam em relacao aos demais.
    st.info("Pizza opcional. Se não for usada, apague esta seção e explique a escolha no comentário.")


if __name__ == "__main__":
    # python -m streamlit run tarefa_02_generos.py
    st.set_page_config(page_title="Tarefa 02 — Gêneros", layout="wide")
    base = carregar_base()
    imprimir_colunas(base)
    exibir(base)
