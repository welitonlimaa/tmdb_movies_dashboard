"""Tarefa 04 — avaliacao do publico e popularidade.

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

import altair as alt
import pandas as pd
import streamlit as st

from preparacao import carregar_base, filmes_para_avaliacao, imprimir_colunas

def exibir(base: pd.DataFrame) -> None:
    """Mostra a secao desta tarefa no dashboard."""
    cor_dispersao = "#14B8A6"
    cor_linha = "#F59E0B"
    nomes_faixa = {"baixa": "Baixa", "media": "Média", "alta": "Alta"}

    st.header("3. Avaliação e popularidade", divider="gray")
    st.info(
        "**Pergunta:** filmes mais populares são necessariamente os mais bem "
        "avaliados? A nota média do público não é a mesma coisa que o índice "
        "de popularidade."
    )

    filmes = filmes_para_avaliacao(base)
    total_filmes = f"{len(filmes):,}".replace(",", ".")
    st.caption(f"**{total_filmes}** filmes com pelo menos 50 votos.")

    with st.container(border=True):
        st.subheader("Dispersão: popularidade x nota")
        # Grafico 1 — dispersao.
        grafico_dispersao = (
            alt.Chart(filmes[["popularidade", "nota_media"]])
            .mark_circle(size=40, opacity=0.5, color=cor_dispersao)
            .encode(
                x=alt.X(
                    "popularidade:Q",
                    title="Popularidade",
                    scale=alt.Scale(zero=False),
                    axis=alt.Axis(grid=False),
                ),
                y=alt.Y(
                    "nota_media:Q",
                    title="Nota média",
                    scale=alt.Scale(zero=False),
                ),
                tooltip=[
                    alt.Tooltip("popularidade:Q", title="Popularidade", format=".1f"),
                    alt.Tooltip("nota_media:Q", title="Nota média", format=".2f"),
                ],
            )
            .properties(height=420, width="container")
        )
        st.altair_chart(grafico_dispersao)

        # Explicacao:
        # Olhando para a dispersão, os pontos não sobem juntos em diagonal. Na verdade,
        # vemos que os filmes muito populares acabam por ter notas médias muito
        # parecidas com as melhores notas dos filmes menos populares.

    with st.container(border=True):
        st.subheader("Linha: nota média por faixa de popularidade")
        # Grafico 2 — linha.
        filmes = filmes.copy()
        filmes["faixa"] = pd.qcut(
            filmes["popularidade"],
            q=3,
            labels=["baixa", "media", "alta"],
        )
        por_faixa = filmes.groupby("faixa", observed=True)["nota_media"].mean().round(2)

        dados_linha = por_faixa.reset_index()
        dados_linha["faixa"] = dados_linha["faixa"].astype(str).map(nomes_faixa)

        base_linha = alt.Chart(dados_linha).encode(
            x=alt.X(
                "faixa:N",
                sort=list(nomes_faixa.values()),
                title="Faixa de popularidade",
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y(
                "nota_media:Q",
                title="Nota média",
                scale=alt.Scale(domain=[0, 10]),
            ),
        )
        linha = base_linha.mark_line(color=cor_linha, strokeWidth=3)
        pontos = base_linha.mark_point(
            color=cor_linha, filled=True, size=160, opacity=1
        ).encode(
            tooltip=[
                alt.Tooltip("faixa:N", title="Faixa"),
                alt.Tooltip("nota_media:Q", title="Nota média", format=".2f"),
            ]
        )
        grafico_linha = (linha + pontos).properties(height=300, width="container")

        coluna_grafico, coluna_valores = st.columns([3, 1])
        with coluna_grafico:
            st.altair_chart(grafico_linha)
        with coluna_valores:
            for faixa, nota in por_faixa.items():
                st.metric(f"Faixa {nomes_faixa[faixa].lower()}", f"{nota:.2f}")

        # Explicacao:
        # A nota média da faixa alta é quase igual à da baixa, dá muito pouca diferença.
        # Então a resposta é não: ser um filme super popular não garante que ele seja o mais bem avaliado.

if __name__ == "__main__":
    # python -m streamlit run tarefa_04_avaliacao_popularidade.py
    st.set_page_config(page_title="Tarefa 04 — Avaliação e popularidade", layout="wide")
    base = carregar_base()
    imprimir_colunas(base)
    exibir(base)

# CONCLUSAO DA TAREFA 5 — AVALIACAO E POPULARIDADE
# A análise demonstrou que os filmes com maior popularidade
# apresentam nota média superior aos filmes menos populares.
# A faixa de baixa popularidade apresentou média de 6,05,
# enquanto a faixa de alta popularidade apresentou média de 6,66.
# Isso indica uma tendência positiva entre popularidade e avaliação,
# mas ser popular não garante uma avaliação elevada do público.
