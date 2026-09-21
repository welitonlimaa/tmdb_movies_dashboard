"""Carrega a base TMDB e devolve uma tabela padronizada para as tarefas.

O CSV em disco nao e alterado. A limpeza acontece so na memoria, cada vez
que carregar_base() e chamada.
"""

from pathlib import Path

import sys

import pandas as pd

PASTA_PROJETO = Path(__file__).resolve().parent
CAMINHO_BASE = PASTA_PROJETO / "dados" / "tmdb_5000_movies.csv"

# Filme com poucos votos pode ter nota 10 ou 0 por acaso.
# Abaixo deste numero a nota continua na tabela, mas nota_confiavel fica False.
MIN_VOTOS_NOTA_CONFIAVEL = 50

# Nomes de genero vem em ingles na base. O dashboard usa o nome em portugues.
GENEROS_PT = {
    "Action": "Ação",
    "Adventure": "Aventura",
    "Animation": "Animação",
    "Comedy": "Comédia",
    "Crime": "Crime",
    "Documentary": "Documentário",
    "Drama": "Drama",
    "Family": "Família",
    "Fantasy": "Fantasia",
    "Foreign": "Estrangeiro",
    "History": "História",
    "Horror": "Terror",
    "Music": "Música",
    "Mystery": "Mistério",
    "Romance": "Romance",
    "Science Fiction": "Ficção científica",
    "TV Movie": "Filme de TV",
    "Thriller": "Suspense",
    "War": "Guerra",
    "Western": "Faroeste",
}

# coluna padronizada -> (nome original no CSV, o que significa)
COLUNAS = {
    "id_filme": (
        "id",
        "Número único do filme. Use este campo para não confundir filmes com o mesmo título.",
    ),
    "titulo": ("title", "Nome do filme exibido ao público."),
    "data_lancamento": ("release_date", "Dia em que o filme foi lançado."),
    "ano": ("release_date", "Ano do lançamento, extraído da data."),
    "generos": (
        "genres",
        "Lista de gêneros do filme, em português. Um filme pode ter vários gêneros.",
    ),
    "orcamento": (
        "budget",
        "Gasto para produzir o filme, em dólares. Zero no CSV significa não informado e vira vazio aqui.",
    ),
    "receita": (
        "revenue",
        "Dinheiro arrecadado pelo filme, em dólares. Zero no CSV significa não informado e vira vazio aqui.",
    ),
    "lucro": (
        "revenue - budget",
        "Receita menos orçamento. Só existe quando os dois valores foram informados.",
    ),
    "retorno": (
        "revenue / budget",
        "Quantas vezes a receita cobriu o orçamento. 2 significa que arrecadou o dobro do que gastou.",
    ),
    "popularidade": (
        "popularity",
        "Índice de popularidade calculado pelo TMDB. Não é a nota do público.",
    ),
    "nota_media": (
        "vote_average",
        "Nota média do público, de 0 a 10. Fica vazia quando ninguém votou.",
    ),
    "quantidade_votos": ("vote_count", "Quantidade de pessoas que deram nota ao filme."),
    "nota_confiavel": (
        "vote_count",
        "True quando há pelo menos 50 votos. Notas com poucos votos enganam a comparação.",
    ),
    "duracao_minutos": (
        "runtime",
        "Duração do filme em minutos. Zero no CSV vira vazio.",
    ),
    "idioma_original": (
        "original_language",
        "Sigla do idioma original, em minúsculas. Exemplo: en para inglês.",
    ),
    "status": ("status", "Situação do filme. A maior parte está como Released (lançado)."),
    "lancado": ("status", "True quando o status é Released."),
}


def _imprimir(texto: str) -> None:
    """Imprime mesmo quando o terminal do Windows nao aceita acento."""
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    seguro = texto.encode(encoding, errors="replace").decode(encoding, errors="replace")
    print(seguro)


def imprimir_colunas(base: pd.DataFrame) -> None:
    """Escreve os labels (nomes das colunas) no terminal, uma vez por processo."""
    if getattr(imprimir_colunas, "ja_impresso", False):
        return

    _imprimir("Colunas (labels) da base padronizada:")
    for nome in base.columns:
        origem, texto = COLUNAS.get(nome, ("", ""))
        if origem:
            _imprimir(f"- {nome} (origem: {origem}): {texto}")
        else:
            _imprimir(f"- {nome}")
    _imprimir(f"Total de filmes: {len(base)}")
    imprimir_colunas.ja_impresso = True


def descricao_colunas(base: pd.DataFrame) -> pd.DataFrame:
    """Tabela com o nome de cada coluna e o que ela significa, para mostrar na tela."""
    linhas = []
    for nome in base.columns:
        origem, texto = COLUNAS.get(nome, ("", ""))
        linhas.append(
            {
                "coluna": nome,
                "coluna_original": origem,
                "significado": texto,
            }
        )
    return pd.DataFrame(linhas)


def _nomes_generos(texto: str) -> list[str]:
    """Le o texto de generos do CSV e devolve a lista de nomes em portugues."""
    if not isinstance(texto, str) or texto.strip() in ("", "[]"):
        return []

    import json

    try:
        itens = json.loads(texto)
    except json.JSONDecodeError:
        return []

    nomes = []
    for item in itens:
        if not isinstance(item, dict):
            continue
        nome_original = str(item.get("name", "")).strip()
        if not nome_original:
            continue
        nomes.append(GENEROS_PT.get(nome_original, nome_original))
    return nomes


def _numero_vazio_quando_zero(serie: pd.Series) -> pd.Series:
    """Converte para numero e troca 0 por vazio.

    Na base original, 0 em orcamento, receita ou duracao quase sempre
    quer dizer que o valor nao foi preenchido, nao que o filme custou nada.
    """
    numero = pd.to_numeric(serie, errors="coerce")
    return numero.mask(numero == 0)


def padronizar(bruto: pd.DataFrame) -> pd.DataFrame:
    """Transforma o CSV cru na tabela usada pelas tarefas."""
    data_lancamento = pd.to_datetime(bruto["release_date"], errors="coerce")
    orcamento = _numero_vazio_quando_zero(bruto["budget"])
    receita = _numero_vazio_quando_zero(bruto["revenue"])
    nota = pd.to_numeric(bruto["vote_average"], errors="coerce")
    votos = pd.to_numeric(bruto["vote_count"], errors="coerce").fillna(0).astype(int)
    nota = nota.mask(votos == 0)

    base = pd.DataFrame(
        {
            "id_filme": pd.to_numeric(bruto["id"], errors="coerce").astype("Int64"),
            "titulo": bruto["title"].fillna("").str.strip(),
            "data_lancamento": data_lancamento,
            "ano": data_lancamento.dt.year,
            "generos": bruto["genres"].apply(_nomes_generos),
            "orcamento": orcamento,
            "receita": receita,
            "popularidade": pd.to_numeric(bruto["popularity"], errors="coerce"),
            "nota_media": nota,
            "quantidade_votos": votos,
            "duracao_minutos": _numero_vazio_quando_zero(bruto["runtime"]),
            "idioma_original": bruto["original_language"].fillna("").str.strip().str.lower(),
            "status": bruto["status"].fillna("").str.strip(),
        }
    )
    base["lancado"] = base["status"].eq("Released")
    base["lucro"] = base["receita"] - base["orcamento"]
    base["retorno"] = base["receita"] / base["orcamento"]
    base["nota_confiavel"] = base["quantidade_votos"] >= MIN_VOTOS_NOTA_CONFIAVEL
    ordem = [
        "id_filme",
        "titulo",
        "data_lancamento",
        "ano",
        "generos",
        "orcamento",
        "receita",
        "lucro",
        "retorno",
        "popularidade",
        "nota_media",
        "quantidade_votos",
        "nota_confiavel",
        "duracao_minutos",
        "idioma_original",
        "status",
        "lancado",
    ]
    return base[ordem]


def carregar_base() -> pd.DataFrame:
    """Le o CSV e devolve a base ja limpa."""
    if not CAMINHO_BASE.exists():
        raise FileNotFoundError(
            f"Nao encontrei a base em {CAMINHO_BASE}. "
            "O arquivo tmdb_5000_movies.csv precisa estar na pasta dados."
        )
    bruto = pd.read_csv(CAMINHO_BASE)
    return padronizar(bruto)


def filmes_com_dinheiro(base: pd.DataFrame) -> pd.DataFrame:
    """Filmes lancados em que orcamento e receita foram informados.

    Use esta tabela na tarefa de orcamento x receita. Sem este filtro,
    os zeros antigos (agora vazios) sumiriam do grafico ou, se voltassem
    como zero, pareceriam filmes de graca.
    """
    return base.loc[
        base["lancado"] & base["orcamento"].notna() & base["receita"].notna()
    ].copy()


def filmes_para_avaliacao(base: pd.DataFrame) -> pd.DataFrame:
    """Filmes lancados cuja nota tem pelo menos 50 votos."""
    return base.loc[base["lancado"] & base["nota_confiavel"]].copy()


def filmes_por_genero(base: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por filme e genero.

    Um filme com 3 generos aparece 3 vezes. Por isso, somar a receita
    desta tabela conta o mesmo dinheiro mais de uma vez. Para comparar
    generos, prefira a media (veja resumo_por_genero).
    """
    longo = base.explode("generos").rename(columns={"generos": "genero"})
    longo = longo.loc[longo["genero"].notna() & (longo["genero"] != "")]
    return longo.reset_index(drop=True)


def resumo_por_genero(base: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por genero, com medias (nao somas) dos filmes lancados.

    A media evita contar duas vezes a receita de um filme que tem mais
    de um genero. A nota media usa apenas filmes com nota confiavel.
    """
    longo = filmes_por_genero(base)
    longo = longo.loc[longo["lancado"]].copy()
    longo["nota_para_media"] = longo["nota_media"].where(longo["nota_confiavel"])

    resumo = longo.groupby("genero", as_index=False).agg(
        quantidade_filmes=("id_filme", "nunique"),
        popularidade_media=("popularidade", "mean"),
        receita_media=("receita", "mean"),
        nota_media=("nota_para_media", "mean"),
    )
    resumo["popularidade_media"] = resumo["popularidade_media"].round(2)
    resumo["receita_media"] = resumo["receita_media"].round(0)
    resumo["nota_media"] = resumo["nota_media"].round(2)
    return resumo.sort_values("receita_media", ascending=False).reset_index(drop=True)


if __name__ == "__main__":
    tabela = carregar_base()
    imprimir_colunas(tabela)
    print("Filmes com orcamento e receita:", len(filmes_com_dinheiro(tabela)))
    print("Filmes com nota confiavel:", len(filmes_para_avaliacao(tabela)))
    print("Generos:", ", ".join(resumo_por_genero(tabela)["genero"].tolist()))
