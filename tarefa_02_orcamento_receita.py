import altair as alt
import streamlit as st
import pandas as pd


from preparacao import carregar_base, filmes_com_dinheiro, imprimir_colunas


def exibir(base: pd.DataFrame) -> None:
    """Mostra a secao desta tarefa no dashboard."""

    st.header("1. Orçamento e receita")

    st.caption(
        "Pergunta: filmes com maior orçamento geram maior receita? "
        "Os gráficos desta seção usam apenas filmes lançados com os dois valores informados."
    )

    filmes = filmes_com_dinheiro(base)

    st.caption(f"{len(filmes)} filmes entram nesta comparação.")

    coluna_dispersao, coluna_barras = st.columns(2, gap="medium", wrap=False)

    with coluna_dispersao:
        with st.container(border=True, key="card_dispersao_orcamento"):
            st.subheader("Dispersão: orçamento x receita")
            grafico = (
                alt.Chart(filmes)
                .mark_circle(size=60)
                .encode(
                    x=alt.X("orcamento:Q", scale=alt.Scale(type="log"), title="Orçamento"),
                    y=alt.Y("receita:Q", scale=alt.Scale(type="log"), title="Receita"),
                    tooltip=["titulo", "orcamento", "receita"],
                )
                .properties(height=320, width="container")
            )
            st.altair_chart(grafico, width="stretch")

    # Explicacao:
    # O grafico de dispersao permite observar a relacao entre
    # orcamento e receita dos filmes. Nota-se uma tendencia de
    # crescimento da receita conforme o orcamento aumenta,
    # indicando uma correlacao positiva entre as variaveis.
    # Entretanto, existem excecoes, com filmes caros que nao
    # arrecadaram proporcionalmente e filmes mais baratos com
    # grande sucesso comercial.

    with coluna_barras:
        with st.container(border=True, key="card_barras_receita"):
            st.subheader("Barras: 10 maiores receitas")

            top = (
                filmes.nlargest(10, "receita")
                .set_index("titulo")[["orcamento", "receita"]]
            )
            # Mesmas barras, na horizontal, para o título caber no cartão.
            longo = top.reset_index().melt(
                id_vars="titulo",
                var_name="serie",
                value_name="valor",
            )
            grafico_barras = (
                alt.Chart(longo)
                .mark_bar()
                .encode(
                    y=alt.Y(
                        "titulo:N",
                        sort=list(top.index),
                        title=None,
                        axis=alt.Axis(
                            labelLimit=180,
                            labelFontSize=10,
                            labelOverlap=False,
                        ),
                    ),
                    x=alt.X("valor:Q", stack="zero", title=None),
                    color=alt.Color(
                        "serie:N",
                        title=None,
                        scale=alt.Scale(
                            domain=["orcamento", "receita"],
                            range=["#1d4ed8", "#7dd3fc"],
                        ),
                        legend=alt.Legend(orient="bottom"),
                    ),
                    order=alt.Order("serie:N", sort="ascending"),
                    tooltip=["titulo", "serie", "valor"],
                )
                .properties(height=320, width="container")
            )
            st.altair_chart(grafico_barras, width="stretch")

    # Explicacao:
    # Entre os 10 filmes com maior receita, percebe-se que
    # grandes orcamentos costumam aparecer entre as maiores
    # arrecadacoes. No entanto, a ordem dos gastos nao segue
    # exatamente a ordem das receitas, indicando que fatores
    # como marketing, franquias conhecidas e aceitacao do
    # publico tambem influenciam o resultado financeiro.


if __name__ == "__main__":
    st.set_page_config(
        page_title="Tarefa 02 — Orçamento e receita",
        layout="wide"
    )

    base = carregar_base()
    imprimir_colunas(base)
    exibir(base)

    # CONCLUSAO DA TAREFA 5 — ORCAMENTO E RECEITA
# A análise de 3.228 filmes com orçamento e receita informados
# identificou uma correlação positiva de aproximadamente 0,705.
# Isso indica que filmes com maiores orçamentos tendem a apresentar
# maiores receitas. Entretanto, essa relação não significa que
# investir mais necessariamente garante maior arrecadação.