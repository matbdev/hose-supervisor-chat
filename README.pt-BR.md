# Supervisor de Mangueiras - Analytics

[Read this in English](README.md)

![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=Databricks&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

Este projeto consiste em uma interface web baseada em Streamlit desenvolvida para atuar como o front-end interativo do Agente Supervisor e Estrategista de Inteligência de Vendas e Supply Chain hospedado no Databricks.

## Índice

- [O Problema](#o-problema)
- [Arquitetura dos Agentes](#arquitetura-dos-agentes)
  - [O Porteiro (Gatekeeper)](#o-porteiro-gatekeeper)
  - [Os Especialistas de Dados](#os-especialistas-de-dados)
  - [O Estrategista](#o-estrategista)
- [Arquitetura Front-End](#arquitetura-front-end)
- [Persistência e Histórico](#persistência-e-histórico)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Configurar e Executar](#como-configurar-e-executar)
  - [Configuração de Variáveis de Ambiente](#configuração-de-variáveis-de-ambiente)
  - [Execução via Docker (Recomendado)](#execução-via-docker-recomendado)
  - [Execução Local](#execução-local)

---

## O Problema

A interface padrão de agentes do Databricks (Playground) possui limitações significativas de renderização UI/UX, especialmente no que tange à geração dinâmica de gráficos interativos (Plotly/ECharts) e manipulação fluida de DataFrames em ambientes de orquestração de agentes (onde um agente supervisor chama outros agentes, no meu caso, estruturados como Genies, para responder o usuário).

Esta aplicação em Streamlit soluciona essa restrição. A orquestração das ferramentas, cruzamentos de dados e a inferência dos modelos LLM permanecem centralizadas no back-end (Databricks), enquanto as respostas estruturadas via JSON são capturadas e processadas nativamente em Python para a renderização limpa e profissional visual de insights e Business Intelligence.

---

## Arquitetura dos Agentes

O escopo do projeto atende exclusivamente à família de produtos de "Mangueiras". O roteamento obedece a um pipeline estruturado e validado.

### O Porteiro (Gatekeeper)
Para qualquer questionamento envolvendo um SKU ou código específico de produto, o agente primeiramente aciona a função `check_is_hose`. Caso a validação retorne falso indicando que o produto não consta ou foge à categoria de Mangueiras, o agente possui a autonomia e governança necessárias para interromper a execução do fluxo analítico imediatamente.

### Os Especialistas de Dados
A arquitetura proíbe adivinhação estatística, dependendo unicamente de funções determinísticas orquestradas baseadas num prompt de roteamento rigoroso:

- **Volume e Margem:** Responsável pela fotografia estática de resultados (Margem Bruta, CPV, Receita Pura). Apura de forma exata faturamentos de clientes ou mercadorias e lucros em períodos fechados.
- **Análise de Variação:** O especialista investigativo estrutural. Trabalha com cruzamento de janelas temporais de vendas pontuais, calculando Deltas percentuais para apontar top ofensores, evasão de clientes (Churn) e maiores alavancadores, com análises focadas apenas no ramo de vendas brutas.
- **Estoque:** Avalia o fluxo físico e inventário, reportando produtos bloqueados, em controle de qualidade ou disponíveis nas prateleiras. Ativado usualmente para validar hipóteses de rupturas em produtos que sofreram quedas abruptas de faturamento.
- **Produção:** Analisa o Work In Progress (WIP) no chão de fábrica, atrasos produtivos, cronogramas de ordens de fabricação pendentes e gargalos temporais nas linhas de montagem, respondendo à premissa "quando o produto estará disponível?".

### O Estrategista
Ao obter todos os dados cruzados das áreas anteriores, o Supervisor assume o papel de Estrategista de Consultoria. A resposta entregue ao usuário é executiva, traçando conexões inteligentes (exemplo: a queda acentuada do faturamento em um SKU em X% ocorreu por uma parada e atraso nos ciclos da Produção). Planos de ação focados são gerados em formato unificado no corpo do chat, enquanto gráficos complementares ilustram a métrica.

---

## Arquitetura Front-End

- **Framework Core:** `Streamlit` para controle responsivo de requisições.
- **Motor Gráfico:** `Plotly` para visualização de dados dinâmica e interativa.
- **Isolamento Modular:** Código organizado em pacotes utilitários (`app/utils`) e esquemas de dados (`app/schemas`).
- **Comentários de Código:** Toda a documentação técnica interna do código está em **Inglês** para manter padrões internacionais de desenvolvimento.

---

## Persistência e Histórico

Diferente de sistemas puramente *stateless*, este projeto implementa persistência total:
- **Banco de Dados:** Utiliza **PostgreSQL** para armazenar conversas.
- **ORM:** **SQLAlchemy** gerencia a camada de dados e esquemas.
- **Histórico Lateral:** O menu lateral (Sidebar) carrega dinamicamente as conversas passadas do banco, permitindo retomar análises anteriores com um clique.

---

## Estrutura do Projeto

```text
supervisor-mangueiras/
├── app/                      # Código fonte da aplicação
│   ├── assets/               # Imagens e logotipos
│   ├── config/               # Configurações de banco (engine)
│   ├── schemas/              # Modelos de dados (SQLAlchemy)
│   ├── utils/                # Utilitários (Extração, UI, DB, Plotly)
│   └── app.py                # Ponto de entrada do Streamlit
├── .streamlit/               # Configurações do Streamlit
├── .dockerignore             
├── .env                      # Variáveis de ambiente (Segredos e Hosts)
├── .gitignore                
├── docker-compose.yml        # Manifesto para execução Dockerizada multi-serviços
├── Dockerfile                # Receita do SO + Framework para ambiente conteinerizado
├── requirements.txt          # Dependências de execução
├── run.py                    # Script auxiliar de execução
└── README.md                 # Você está aqui
```

---

## Como Configurar e Executar

### Configuração de Variáveis de Ambiente

Crie um arquivo `.env` na raiz do repositório contendo as credenciais da conta Databricks e a origem do Endpoint do Agente:

```env
# Databricks
DATABRICKS_HOST=https://seu-workspace.databricks.com
DATABRICKS_TOKEN=seu_token
ENDPOINT_NAME=seu_endpoint

# Banco de Dados
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_DB=supervisor_db
DB_HOST=postgres-db
DB_PORT=5432
```

### Execução Local (Virtual Environment)

Para rodar a aplicação nativamente separando todas as dependências no seu ambiente, recomenda-se a utilização de um `venv` nativo do Python:

1. **Crie o ambiente virtual (venv):**
```bash
python -m venv venv
```

2. **Ative o ambiente:**
- Em Windows (Prompt/PowerShell):
  ```bash
  venv\Scripts\activate
  ```
- Em Linux / macOS:
  ```bash
  source venv/bin/activate
  ```

3. **Instale as dependências requeridas no repositório:**
```bash
pip install -r requirements.txt
```

4. **Inicie o servidor Streamlit:**
```bash
streamlit run app.py
```

### Execução via Docker (Recomendado)

O projeto utiliza `docker-compose` para subir tanto a interface quanto o banco de dados de forma integrada:

1. Realize o build da imagem em Docker e inicie os serviços em modo detach:
```bash
docker-compose up -d --build
```
Acesse em: `http://localhost:8501`.

### Execução Local

1. Instale as dependências: `pip install -r requirements.txt`
2. Garanta que possui um Postgres rodando localmente e ajuste o `.env`.
3. Execute via script facilitador:
```bash
python run.py
```
