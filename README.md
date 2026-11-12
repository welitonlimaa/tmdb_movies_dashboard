# Análise do desempenho de filmes

Dashboard do Grupo 6 para o Projeto Integrador de Ciência de Dados (Senac).
A página junta três tarefas. Cada objetivo específico do projeto é um arquivo.
A biblioteca da tela é o Streamlit. A tabela é lida com o Pandas.

Integrantes:

- Darlan José de Oliveira
- Weliton Pereira Lima Junior
- Jonathas dos Santos Fideles
- Silvana dos Santos Vieira
- Alexander Nascimento Santos
- Richardson da Silva Freitas

## O que o dashboard precisa responder

O objetivo geral é analisar o desempenho dos filmes relacionando gênero, orçamento, receita, popularidade e avaliação do público.

Cada objetivo específico é uma tarefa, com o próprio arquivo:

| Arquivo | Pergunta | Gráficos |
|---|---|---|
| `tarefa_02_orcamento_receita.py` | Filmes com maior orçamento geram maior receita? | Dispersão (orçamento x receita) e barras dos 10 filmes de maior receita |
| `tarefa_03_generos.py` | Quais gêneros têm maior popularidade e receita? | Barras de receita média por gênero e barras de popularidade média. Pizza só se ficar nos 5 gêneros do topo |
| `tarefa_04_avaliacao_popularidade.py` | Filmes mais populares são os mais bem avaliados? | Dispersão (popularidade x nota) e linha da nota média por faixa de popularidade |

O arquivo `app.py` é o dashboard final. Ele mostra o título, três cartões (KPI) e chama as três tarefas, uma embaixo da outra. Juntos, os cartões e os gráficos passam do mínimo de 4 visualizações pedido na etapa 2.

A explicação do que cada gráfico mostra (a conclusão) fica como **comentário no código**, ao lado do gráfico. Não crie um arquivo separado só para esse texto. No lugar marcado com `Explicacao (comentario obrigatorio)`, escreva em uma ou duas frases o que os dados mostraram. Exemplo de formato, dentro do arquivo da tarefa:

```python
# Explicacao: entre os filmes com orcamento e receita informados,
# gastar mais nao garante arrecadar mais. Varios filmes caros
# ficam abaixo de filmes com orcamento menor.
```

As três conclusões pedidas na etapa 2 saem desses comentários (uma por tarefa, apoiada no gráfico). Na entrega, enviem também o print da tela.

## Como a pasta está organizada

```text
app.py                              pagina que junta tudo
preparacao.py                       leitura e limpeza da base
tarefa_02_orcamento_receita.py     objetivo 1
tarefa_03_generos.py               objetivo 2
tarefa_04_avaliacao_popularidade.py objetivo 3
requirements.txt                    bibliotecas para instalar
dados/tmdb_5000_movies.csv          base de filmes
```

Quem mexe na tarefa 2 edita só `tarefa_02_orcamento_receita.py`. O mesmo vale para as outras. O gráfico escrito na tarefa aparece no dashboard porque o `app.py` já chama as três funções `exibir`.

## A base de dados

Fonte: [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata), arquivo `tmdb_5000_movies.csv` (4.803 filmes). O arquivo já está em `dados/`. Não é preciso baixar de novo.

O outro arquivo do Kaggle (`tmdb_5000_credits.csv`, elenco e equipe) não entra neste projeto. Nenhum objetivo específico usa elenco.

O CSV original não é alterado. `preparacao.py` lê o arquivo e devolve uma tabela nova, com nomes em português. Para ver os nomes das colunas (os labels) no terminal:

```text
python preparacao.py
```

Cada arquivo de tarefa também carrega a base e imprime esses labels quando é executado.

O que a limpeza faz, e por quê:

- **Gênero** vinha como texto com vários nomes no mesmo campo, em inglês. Vira uma lista em português (`Ação`, `Comédia`, `Ficção científica` e assim por diante).
- **Orçamento, receita e duração iguais a zero** viram vazio. No TMDB, zero quase sempre significa "não informaram", não que o filme custou nada ou durou zero minutos.
- **Lucro** é receita menos orçamento. **Retorno** é receita dividida pelo orçamento. Os dois só existem quando orçamento e receita foram informados.
- **Nota sem nenhum voto** fica vazia. **Nota confiável** é `True` quando há pelo menos 50 votos. Uma nota 10 com um voto só não serve para comparar filmes.
- **Lançado** é `True` quando o status original é `Released`.

Funções prontas para usar nas tarefas:

- `carregar_base()` — tabela limpa, uma linha por filme.
- `filmes_com_dinheiro(base)` — só filmes lançados com orçamento e receita. Use na tarefa 2.
- `resumo_por_genero(base)` — uma linha por gênero, com médias. Use na tarefa 3. A média evita contar duas vezes o dinheiro de um filme que tem mais de um gênero.
- `filmes_para_avaliacao(base)` — filmes lançados com pelo menos 50 votos. Use na tarefa 4.
- `imprimir_colunas(base)` — escreve os labels no terminal.

Colunas que as tarefas usam: `titulo`, `generos`, `orcamento`, `receita`, `lucro`, `retorno`, `popularidade`, `nota_media`, `quantidade_votos`, `nota_confiavel`, `ano`. Os valores de dinheiro estão em dólares, como na base original.

Três filmes compartilham o título com outro filme. O `id_filme` é único. Se for mostrar um título na tela e houver dúvida, use o id.

## Como rodar no computador

É preciso o Python 3.11 ou mais novo. Na instalação, marque **Add python.exe to PATH**.

Abra o terminal **na pasta deste projeto** e rode, um comando por vez:

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

O navegador abre em `http://localhost:8501`. Se não abrir, copie esse endereço.

Para ver só uma tarefa:

```text
python -m streamlit run tarefa_01_orcamento_receita.py
```

Troque o nome do arquivo pela tarefa 2 ou 3 se for o caso.

Para encerrar, volte ao terminal e pressione `Ctrl+C`.

Na próxima vez, se a pasta `.venv` já existir, basta ativar e rodar de novo:

```text
.venv\Scripts\activate
python -m streamlit run app.py
```

## Como completar uma tarefa

1. Abra o arquivo da sua tarefa.
2. Onde está `st.info(...)`, apague o aviso e descomente o exemplo de gráfico (tire o `#` do início da linha), ou escreva o seu.
3. Salve o arquivo. Com o dashboard aberto, a página atualiza sozinha. Confira se o gráfico apareceu. Se a página não atualizar, volte ao terminal do Streamlit e pressione a tecla `R`.
4. Ao lado do gráfico, escreva a conclusão como comentário. Comentário em Python começa com `#`.
5. Não apague o `import` do começo do arquivo nem a chamada `imprimir_colunas`.

Comandos de gráfico que já vêm com o Streamlit (não precisa de outra biblioteca):

```python
st.scatter_chart(filmes, x="orcamento", y="receita")
st.bar_chart(resumo.set_index("genero")[["receita_media"]])
st.line_chart(por_faixa)
st.metric("Filmes na base", "4803")
```

`st.metric` é o cartão (KPI). `st.bar_chart` é o gráfico de barras. `st.line_chart` é o de linha. `st.scatter_chart` é o de dispersão (pontos).

## Git, para o grupo trabalhar junto

O versionamento é Git. Quem cria o repositório no GitHub sobe esta pasta depois. Os PDFs da disciplina ficam de fora de propósito (estão no `.gitignore`).

Quando o repositório já existir, cada pessoa baixa uma cópia:

```text
git clone ENDERECO_DO_REPOSITORIO
```

Antes de editar, pegue a versão mais nova:

```text
git pull
```

Depois de mudar o seu arquivo, grave a versão:

```text
git status
git add tarefa_01_orcamento_receita.py
git commit -m "adiciona graficos de orcamento e receita"
git push
```

Troque o nome do arquivo e a mensagem pelo que você fez de fato. `git status` mostra o que mudou. `git add` escolhe o arquivo. `git commit` grava um ponto na história. `git push` envia para o GitHub.

Evite duas pessoas editarem o mesmo arquivo ao mesmo tempo. Cada objetivo já tem o seu arquivo para isso.
