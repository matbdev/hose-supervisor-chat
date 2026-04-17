# Hose Supervisor - Analytics

[Leia isto em Português](README.pt-BR.md)

![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=Databricks&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

This project consists of a Streamlit-based web interface developed to act as the interactive front-end for the Sales Intelligence and Supply Chain Sales Supervisor and Strategist Agent hosted on Databricks.

## Index

- [The Problem](#the-problem)
- [Agent Architecture](#agent-architecture)
  - [The Gatekeeper](#the-gatekeeper)
  - [Data Specialists](#data-specialists)
  - [The Strategist](#the-strategist)
- [Front-End Architecture](#front-end-architecture)
- [Persistence and History](#persistence-and-history)
- [Project Structure](#project-structure)
- [How to Configure and Run](#how-to-configure-and-run)
  - [Environment Variables Configuration](#environment-variables-configuration)
  - [Running via Docker (Recommended)](#running-via-docker-recommended)
  - [Local Execution](#local-execution)

---

## The Problem

The default Databricks agent interface (Playground) has significant UI/UX rendering limitations, especially regarding the dynamic generation of interactive charts (Plotly/ECharts) and fluid manipulation of DataFrames in agent orchestration environments (where a supervisor agent calls other agents, in my case, structured as Genies, to respond to the user).

This Streamlit application solves this restriction. The tool orchestration, data crossing, and LLM model inference remain centralized in the back-end (Databricks), while structured JSON responses are captured and processed natively in Python for clean and professional visual rendering of insights and Business Intelligence.

---

## Agent Architecture

The project scope exclusively serves the "Hoses" product family. Routing follows a structured and validated pipeline.

### The Gatekeeper

For any inquiry involving a specific SKU or product code, the agent first triggers the `check_is_hose` function. If the validation returns false, indicating the product is not in the Hoses category, the agent has the necessary autonomy and governance to immediately stop the analytical flow execution.

### Data Specialists

The architecture prohibits statistical guessing, depending solely on deterministic functions based on a rigorous routing prompt:

- **Volume and Margin:** Responsible for the static photography of results (Gross Margin, COGS, Net Revenue). It exactly calculates customer or merchandise billing and profits in closed periods.
- **Trend Analysis:** The structural investigative specialist. It works by crossing specific sales time windows, calculating percentage Deltas to point out top offenders, customer churn, and major levers, focusing only on the gross sales branch.
- **Inventory:** Evaluates physical flow and inventory, reporting blocked, quality-controlled, or shelf-available products. Usually activated to validate rupture hypotheses in products that suffered abrupt billing drops.
- **Production:** Analyzes Work In Progress (WIP) on the factory floor, production delays, pending manufacturing order schedules, and temporal bottlenecks in assembly lines, answering the premise "when will the product be available?".

### The Strategist

Upon obtaining all crossed data from the previous areas, the Supervisor assumes the role of Consulting Strategist. The response delivered to the user is executive, drawing smart connections (example: the sharp drop in billing in an SKU by X% occurred due to a stop and delay in Production cycles). Focused action plans are generated in a unified format in the chat body, while complementary charts illustrate the metric.

---

## Front-End Architecture

- **Core Framework:** `Streamlit` for responsive request control.
- **Graphics Engine:** `Plotly` for dynamic and interactive data visualization.
- **Modular Isolation:** Code organized into utility packages (`app/utils`) and data schemas (`app/schemas`).
- **Code Comments:** All internal technical code documentation is in **English** to maintain international development standards.

---

## Persistence and History

Unlike purely stateless systems, this project implements full persistence:

- **Database:** Uses **PostgreSQL** to store conversations.
- **ORM:** **SQLAlchemy** manages the data layer and schemas.
- **Sidebar History:** The sidebar menu dynamically loads past conversations from the database, allowing previous analyses to be resumed with one click.

---

## Project Structure

```text
supervisor-mangueiras/
├── app/                      # Application source code
│   ├── assets/               # Images and logos
│   ├── config/               # Database configurations (engine)
│   ├── schemas/              # Data models (SQLAlchemy)
│   ├── utils/                # Utilities (Extraction, UI, DB, Plotly)
│   └── app.py                # Streamlit entry point
├── .streamlit/               # Streamlit configurations
├── .dockerignore
├── .env                      # Environment variables (Secrets and Hosts)
├── .gitignore
├── docker-compose.yml        # Manifesto for multi-service Dockerized execution
├── Dockerfile                # OS Recipe + Framework for containerized environment
├── requirements.txt          # Execution dependencies
├── run.py                    # Auxiliary execution script
└── README.md                 # You are here
```

---

## How to Configure and Run

### Environment Variables Configuration

Create a `.env` file at the root of the repository containing Databricks account credentials and the Agent Endpoint source:

```env
# Databricks
DATABRICKS_HOST=https://your-workspace.databricks.com
DATABRICKS_TOKEN=your_token
ENDPOINT_NAME=your_endpoint
CHART_DATA_JSON_FUNCTION=your_function_that_converts_data_into_json_on_databricks

# Database
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=supervisor_db
DB_HOST=postgres-db
DB_PORT=5432
```

### Local Execution (Virtual Environment)

To run the application natively by separating all dependencies in your environment, it is recommended to use a native Python `venv`:

1. **Create the virtual environment (venv):**

```bash
python -m venv venv
```

2. **Activate the environment:**

- On Windows (Prompt/PowerShell):
  ```bash
  venv\Scripts\activate
  ```
- On Linux / macOS:
  ```bash
  source venv/bin/activate
  ```

3. **Install required dependencies in the repository:**

```bash
pip install -r requirements.txt
```

4. **Start the Streamlit server:**

```bash
streamlit run app.py
```

### Running via Docker (Recommended)

The project uses `docker-compose` to spin up both the interface and the database in an integrated way:

1. Build the Docker image and start the services in detach mode:

```bash
docker-compose up -d --build
```

Access at: `http://localhost:8501`.

### Local Execution

1. Install dependencies: `pip install -r requirements.txt`
2. Ensure you have a local Postgres running and adjust the `.env`.
3. Run via helper script:

```bash
python run.py
```
