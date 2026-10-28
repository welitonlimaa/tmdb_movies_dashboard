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

    st.scatter_chart(
        filmes,
        x="orcamento",
        y="receita",
    )

    # Explicacao:
    # O grafico de dispersao permite observar a relacao entre
    # orcamento e receita dos filmes. Nota-se uma tendencia de
    # crescimento da receita conforme o orcamento aumenta,
    # indicando uma correlacao positiva entre as variaveis.
    # Entretanto, existem excecoes, com filmes caros que nao
    # arrecadaram proporcionalmente e filmes mais baratos com
    # grande sucesso comercial.

    st.subheader("Barras: 10 maiores receitas")

    top = (
        filmes.nlargest(10, "receita")
        .set_index("titulo")[["orcamento", "receita"]]
    )

    st.bar_chart(top)

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