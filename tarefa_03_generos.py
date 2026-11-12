import altair as alt
import streamlit as st
import pandas as pd

from preparacao import carregar_base, imprimir_colunas, resumo_por_genero


def exibir(base: pd.DataFrame) -> None:
    """Mostra a secao desta tarefa no dashboard."""
    st.header("2. Gêneros, popularidade e receita")
    st.caption(
        "Pergunta: quais gêneros apresentam maior popularidade e receita? "
        "Os números são médias por filme lançado, para não contar duas vezes "
        "quem tem mais de um gênero."
    )

    resumo = resumo_por_genero(base)
    st.caption(f"{len(resumo)} gêneros na base.")

    # Genero sem nenhuma receita informada (ex.: Filme de TV) nao tem media,
    # entao fica fora deste grafico.
    receita = resumo.dropna(subset=["receita_media"]).copy()
    receita["receita_milhoes"] = receita["receita_media"] / 1_000_000

    coluna_receita, coluna_popularidade, coluna_pizza = st.columns(3, gap="medium", wrap=False)

    # ------------------------------------------------------------------
    # Grafico 1 — barras: receita media por genero.
    # ------------------------------------------------------------------
    with coluna_receita:
        with st.container(border=True, key="card_receita_genero"):
            st.subheader("Barras: receita média por gênero")

            grafico_receita = (
                alt.Chart(receita)
                .mark_bar(color="#14B8A6")
                .encode(
                    x=alt.X(
                        "receita_milhoes:Q",
                        title="Receita média por filme (US$ milhões)",
                    ),
                    y=alt.Y(
                        "genero:N",
                        sort="-x",
                        title=None,
                        axis=alt.Axis(
                            labelLimit=140,
                            labelOverlap=False,
                            labelFontSize=11,
                        ),
                    ),  # do maior para o menor
                    tooltip=[
                        alt.Tooltip("genero:N", title="Gênero"),
                        alt.Tooltip("receita_milhoes:Q", title="Receita média (US$ mi)", format=".1f"),
                        alt.Tooltip("quantidade_filmes:Q", title="Filmes lançados"),
                    ],
                )
                .properties(height=320, width="container")
            )
            st.altair_chart(grafico_receita, width="stretch")

    # Explicacao:
    # Animação lidera a receita média (cerca de US$ 277 milhões por filme),
    # seguida de Aventura (244 mi), Fantasia (234 mi) e Família (218 mi).
    # A liderança não é folgada: os quatro primeiros ficam numa faixa
    # parecida. A diferença grande está entre esse grupo e os gêneros de
    # baixo, como Drama (78 mi) e Documentário (23 mi). Gêneros com muitos
    # filmes, como Drama e Comédia, arrecadam bem menos por filme.

    # ------------------------------------------------------------------
    # Grafico 2 — barras: popularidade media por genero.
    # ------------------------------------------------------------------
    with coluna_popularidade:
        with st.container(border=True, key="card_popularidade_genero"):
            st.subheader("Barras: popularidade média por gênero")

            grafico_popularidade = (
                alt.Chart(resumo)
                .mark_bar(color="#F59E0B")
                .encode(
                    x=alt.X("popularidade_media:Q", title="Popularidade média (índice TMDB)"),
                    y=alt.Y(
                        "genero:N",
                        sort="-x",
                        title=None,
                        axis=alt.Axis(
                            labelLimit=140,
                            labelOverlap=False,
                            labelFontSize=11,
                        ),
                    ),
                    tooltip=[
                        alt.Tooltip("genero:N", title="Gênero"),
                        alt.Tooltip("popularidade_media:Q", title="Popularidade média", format=".2f"),
                        alt.Tooltip("quantidade_filmes:Q", title="Filmes lançados"),
                    ],
                )
                .properties(height=320, width="container")
            )
            st.altair_chart(grafico_popularidade, width="stretch")

    # Explicacao:
    # Aventura (39,3) e Animação (38,8) ficam praticamente empatadas no topo,
    # seguidas de Ficção científica (36,5) e Fantasia (36,4). Quatro dos cinco
    # gêneros de maior receita média também estão entre os cinco mais
    # populares, então popularidade e receita andam juntas. As diferenças:
    # Ação entra no top 5 de popularidade, mas não no de receita, e Família
    # tem a 4ª maior receita com popularidade menor (27,9). No fim da lista
    # ficam Estrangeiro, Documentário e Filme de TV, que também são gêneros
    # com poucos filmes na base.

    # ------------------------------------------------------------------
    # Grafico 3 — pizza: so os 5 generos de maior receita media.
    # ------------------------------------------------------------------
    with coluna_pizza:
        with st.container(border=True, key="card_pizza"):
            st.subheader("Pizza: participação dos 5 gêneros de maior receita média")

            top5 = receita.nlargest(5, "receita_media").copy()
            # Participacao = fatia de cada genero dentro do grupo dos 5 (0 a 1).
            top5["participacao"] = top5["receita_media"] / top5["receita_media"].sum()

            base_pizza = alt.Chart(top5).encode(
                theta=alt.Theta("participacao:Q", stack=True),
                color=alt.Color(
                    "genero:N",
                    title="Gênero",
                    legend=alt.Legend(orient="bottom", columns=2),
                ),
                tooltip=[
                    alt.Tooltip("genero:N", title="Gênero"),
                    alt.Tooltip("receita_milhoes:Q", title="Receita média (US$ mi)", format=".1f"),
                    alt.Tooltip("participacao:Q", title="Participação", format=".1%"),
                ],
            )
            pizza = base_pizza.mark_arc(outerRadius=78)
            rotulos = base_pizza.mark_text(radius=98, size=11).encode(
                text=alt.Text("participacao:Q", format=".1%")
            )
            st.altair_chart(
                (pizza + rotulos).properties(height=300, width="container"),
                width="stretch",
            )

    # Explicacao:
    # Dentro do grupo dos 5 maiores, as fatias são parecidas: Animação 23,9%,
    # Aventura 21,1%, Fantasia 20,2%, Família 18,8% e Ficção científica 16,0%.
    # Isso confirma que a liderança é apertada. Somando as médias, esses 5
    # gêneros representam cerca de metade (50%) da soma das médias dos 19
    # gêneros que têm receita informada, ou seja, 5 gêneros concentram o
    # mesmo que os outros 14 juntos. A pizza compara médias por filme, não
    # o total arrecadado por cada gênero.


if __name__ == "__main__":
    # python -m streamlit run tarefa_03_generos.py
    st.set_page_config(page_title="Tarefa 03 — Gêneros", layout="wide")
    base = carregar_base()
    imprimir_colunas(base)
    exibir(base)

    # CONCLUSAO DA TAREFA 5 — GENEROS CINEMATOGRAFICOS
# A análise identificou que Animação, Aventura e Fantasia estão
# entre os gêneros com maiores receitas médias.
# Aventura, Animação e Ficção Científica também se destacam
# em popularidade média.
# Os resultados demonstram que alguns gêneros se destacam
# nos dois indicadores, mas receita e popularidade representam
# medidas diferentes de desempenho dos filmes.
