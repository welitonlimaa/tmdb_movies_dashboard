"""Tarefa 03 — avaliacao do publico e popularidade.

Objetivo especifico:
Comparar a avaliacao dos filmes com sua popularidade.
Verificar se filmes mais populares tambem apresentam melhores avaliacoes.

Graficos desta tarefa (pode haver mais de um):
1. Grafico de dispersao. Eixo X = popularidade, eixo Y = nota_media.
   Cada ponto e um filme. Serve para ver se a nota sobe quando a
   popularidade sobe.
2. Grafico de linha (ou de barras) da nota media por faixa de popularidade.
   Exemplo de faixas: baixa, media e alta. A linha resume a dispersao
   e facilita a resposta direta: a nota acompanha a popularidade ou nao?

Use filmes_para_avaliacao. Ela tira filmes com menos de 50 votos, porque
uma nota 10 com um unico voto nao representa o publico.

A explicacao do resultado deve ser escrita como comentario no codigo,
ao lado de cada grafico. Nao crie outro arquivo so para esse texto.
"""

import streamlit as st
import pandas as pd

from preparacao import carregar_base, filmes_para_avaliacao, imprimir_colunas


def exibir(base: pd.DataFrame) -> None:
    """Mostra a secao desta tarefa no dashboard."""
    st.header("3. Avaliação e popularidade")
    st.write(
        "Pergunta: filmes mais populares são necessariamente os mais bem avaliados? "
        "A nota média do público não é a mesma coisa que o índice de popularidade."
    )

    filmes = filmes_para_avaliacao(base)
    st.caption(f"{len(filmes)} filmes com pelo menos 50 votos.")

    st.subheader("Dispersão: popularidade x nota")
    # Grafico 1 — dispersao.
    # st.scatter_chart(filmes, x="popularidade", y="nota_media")
    #
    # Explicacao (comentario obrigatorio):
    # Diga se os pontos sobem juntos ou se filmes muito populares aparecem
    # com notas medias parecidas com as dos menos populares.
    st.info("Gráfico de dispersão ainda não foi feito. Edite tarefa_03_avaliacao_popularidade.py.")

    st.subheader("Linha: nota média por faixa de popularidade")
    # Grafico 2 — linha.
    # Uma forma simples de criar faixas:
    # filmes = filmes.copy()
    # filmes["faixa"] = pd.qcut(
    #     filmes["popularidade"],
    #     q=3,
    #     labels=["baixa", "media", "alta"],
    # )
    # por_faixa = filmes.groupby("faixa", observed=True)["nota_media"].mean()
    # st.line_chart(por_faixa)
    #
    # Explicacao (comentario obrigatorio):
    # Compare a nota da faixa alta com a da faixa baixa e responda a pergunta
    # do objetivo em uma ou duas frases.
    st.info("Gráfico de linha ainda não foi feito. Edite tarefa_03_avaliacao_popularidade.py.")


if __name__ == "__main__":
    # python -m streamlit run tarefa_03_avaliacao_popularidade.py
    st.set_page_config(page_title="Tarefa 03 — Avaliação e popularidade", layout="wide")
    base = carregar_base()
    imprimir_colunas(base)
    exibir(base)
