**Guilherme Nunes**
# Desafio Stract: Scraper local em Python + Flask 
### Ambiente

- *WSL2 Ubuntu 20.04 + Python 3*

## Setup

```bash
pip3 install -r requirements.txt
python3 server.py
```

## Instruções de uso

Chame as rotas na forma que quiser 
(as rotas estarão disponíveis em `Stract.postman_collection.json` e poderão ser testadas via postman.)
* *Será necessário adicionar o bearer token no collection do postman para poder usar a api de consumo.*

## Considerações

Comecei esse desafio levando em conta todos os requisitos que me foram pedidos, cuidadosamente.

Acredito que não há melhor forma de comprovar que notei todos  se não colocando todas as informações que obtive e separando elas como "regras de negócio" (que estarão abaixo) para esse projeto, e ao mesmo tempo onde também foi considerada uma entrega rápida, eficaz e simples: e propositalmente sem utilizar pandas, procurando se manter um projeto leve.

Ao final, gostaria de justificar que por conta do escopo do projeto escolhi fazer o consumo de dados, parsing, e tratamento no mesmo arquivo (`server.py`), não influenciando em nada sobre os requisitos pedidos. 

Como verão, escolhi utilizar funções unitárias que se repetiram diversas vezes antes de utilizá-las nas rotas, e ao abrir o código primeiro encontrarão elas: 

```python
# -------- funções de consumo e parsing --------
```

E depois as rotas do servidor local, a partir de:

```python
# -------- servidor local e tratamento de retornos requisitados --------
```

Também gostaria de saber sobre a questão do Campo "Cost per Click" (cpc), pois não recebi a resposta do valor "spend" para realizadr a divisão de spend / clicks para esse "cpc", em específico para as plataformas da google analytic e do tiktok que não possuem esse campo "spend". Deixei comentado lá na linha 96.

E no geral, é isso. Caso hajam dúvidas podem me chamar via email ou celular!

## Requisitos essenciais

[x] Tratamento de dados, e apresentá-los como relatórios em forma de tabela.

[x] Extração das contas e campos de cada plataforma.

[x] Extração de os insights relativos aos anúncios de cada conta.

[x] Explorar e entender a API, inclusive suas peculiaridades, contando apenas com a documentação mínima apresentada.

---

## O que eu fiz

[x] Criar um Servidor local que consuma os dados desta API e entregue os relatórios especificados.

[x] Relatórios gerados em tempo real, apresentados em formato CSV com seus devidos cabeçalhos. 

[x] Deve ser implementado em Python+Flask, com o mínimo de dependências possíveis. 

[x] Endpoints devem ter como raiz o localhost na porta padrão [5000], e serem publicamente acessíveis através de um GET.

---

## Requisitos da API

Os relatórios deve ser acessíveis a partir dos seguintes endpoints:
-  `/`
-  `/{{plataforma}}`
-  `/{{plataforma}}/resumo`
-  `/geral`
-  `/geral/resumo`

---

## Requisitos dos Endpoints

### Endpoint: `/`

- [x] A raiz da sua API deve retornar seu nome, email e o link para o LinkedIn

---

### Endpoint: `/{{plataforma}}`

- [x] Deve retornar uma tabela em que cada linha represente um anúncio veiculado na plataforma indicada. 
- [x] As colunas devem trazer todos os campos de insights daquele anúncio, bem como o nome da conta que o está veiculando.
- [x] Nome não é um identificador único

---

### Endpoint: `/{{plataforma}}/resumo`

- [x] Deve trazer uma tabela com todas as linhas que forem da mesma conta, mas colapsando em uma única linha.
- [x] Dados devem ser somados nas colunas numéricas
- [x] Colunas que tem texto: os dados podem ficar vazios (exceto o nome da conta)

---

### Endpoint: `/geral`

- [x] Deve trazer todos os anúncios de todas as plataformas. 
- [x] Devem ser adicionadas colunas para identificar por nome a plataforma na qual o anúncio está sendo veiculado. 
- [x] Devem haver colunas para todos os campos existentes na API. 
- [x] Campo pode ficar vazio nas linhas das plataformas nas quais ele não exista. 
- [!] Campo "Cost per Click" pode ser calculado dividindo-se o valor de "spend" pelo valor de "clicks" (linha )

---

### Endpoint: `/geral/resumo`

- [x] Deve trazer uma tabela similar, mas colapsando em uma única linha todas as linhas que forem da mesma plataforma. 
- [x] Caso as colunas sejam numéricas, os dados devem ser somados.
- [x] Caso sejam texto, a coluna pode ficar vazia na linha em questão (exceto nome da plataforma).