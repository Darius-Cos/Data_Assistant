# Data Assistant | Synthetic Data Generation & Natural-Language SQL

An interactive **Streamlit data assistant** that transforms SQL schemas into synthetic datasets and allows users to ask questions about the resulting data in natural language. The application integrates **Gemini on Vertex AI, PostgreSQL, SQLAlchemy, Pandas, and Langfuse**.

> **Core question:** Can someone explore relational data, create example datasets, and get useful SQL results without writing SQL manually?

## Overview

The application brings together two workflows:

1. **Synthetic Data Generation:** upload a database schema (DDL), generate sample records with an LLM, preview them, edit them using natural-language instructions, and export them as CSV or ZIP.
2. **Talk to Your Data:** ask a business question in plain English, generate a SQL query, run it against PostgreSQL, and display the resulting table or chart.

This is an educational prototype designed to demonstrate LLM-driven data workflows, not a security-hardened production database assistant.

## Main Features

- Parse uploaded `.sql`, `.ddl`, or `.txt` schema files.
- Generate synthetic data for database tables using Gemini.
- Specify generation constraints in natural language (for example, a row count).
- Preview and export generated tables individually or as a ZIP archive.
- Apply text-based edits to previously generated DataFrames.
- Save generated tables to PostgreSQL when a database connection is available.
- Turn natural-language questions into SQL queries and display the generated SQL.
- Execute queries and visualize suitable results with charts.
- Use basic prompt-injection, off-topic, and SQL-query checks.
- Optionally capture LLM observations through Langfuse.

## Application Flow

```text
                    SQL DDL schema
                         |
                         v
                  DDL Parser
                         |
                         v
                 Gemini Generator
                         |
             +-----------+-----------+
             |                       |
             v                       v
      Pandas DataFrames        PostgreSQL Tables
             |                       |
             v                       v
        CSV / ZIP Export      Natural-language Question
                                     |
                                     v
                            Gemini SQL Generation
                                     |
                                     v
                           Query Validation / SQL
                                     |
                                     v
                             Results + Charts
```

## Project Structure

```text
Data_Assistant/
├── app.py                         # Streamlit navigation and UI
├── generator/
│   ├── ddl_parser.py              # Extracts table information from DDL
│   ├── data_generator.py          # Synthetic data creation and editing
│   └── gemini_client.py           # Vertex AI model configuration
├── chat/
│   ├── chat_engine.py             # Chat workflow orchestration
│   ├── sql_generator.py           # Natural language to SQL
│   ├── db_executor.py             # Database query execution
│   └── guardrails.py              # Basic safety checks
├── database/
│   └── db_setup.py                # SQLAlchemy connection and table writes
├── utils/
│   ├── file_utils.py              # CSV / ZIP utilities
│   ├── visualization.py           # Plot generation
│   └── langfuse_client.py         # Optional tracing
├── data/                           # Example DDL schemas
├── Synthetic_Data/                 # Example generated CSV datasets
├── docker-compose.yml             # Local PostgreSQL service
└── requirements.txt
```

## How Each Part Works

### 1. Schema parsing

`generator/ddl_parser.py` processes DDL statements to identify table names and schema information used by the generation workflow.

### 2. Synthetic record generation

`generator/data_generator.py` builds LLM requests from the schema and optional user instructions, converts the responses into Pandas DataFrames, and supports subsequent text-guided edits.

### 3. Text-to-SQL

`chat/sql_generator.py` asks the model to convert a natural-language question into SQL based on the active schema. `chat/guardrails.py` includes simple checks to discourage off-topic requests and reject statements outside its allowed query types.

### 4. Query execution and reporting

`chat/db_executor.py` executes SQL on PostgreSQL, while `utils/visualization.py` attempts to produce suitable visualizations from returned data.

> **Security note:** pattern matching and `SELECT`/`WITH` checks are not a substitute for proper SQL parsing, least-privilege database users, query timeouts, or sandboxing. Use sample data and a restricted database account.

## Technology Stack

| Area | Tool | Purpose |
|---|---|---|
| Language | Python | Application logic |
| UI | Streamlit | Data generation and chat interface |
| LLM | Gemini / Vertex AI | Synthetic data and SQL generation |
| Database | PostgreSQL | Persistent relational data |
| DB access | SQLAlchemy + psycopg2 | Database connectivity |
| Data processing | Pandas | Tabular manipulation |
| Visualization | Matplotlib + Seaborn | Charts |
| Observability | Langfuse | Optional tracing |
| Local infrastructure | Docker Compose | PostgreSQL service |

## Getting Started

### Prerequisites

- Python and pip
- Docker Desktop or a working PostgreSQL instance
- A **personal Google Cloud project** with Vertex AI access
- Google Cloud CLI (`gcloud`) for Application Default Credentials

### 1. Clone the project

```bash
git clone https://github.com/Darius-Cos/Data_Assistant.git
cd Data_Assistant
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Review local database configuration

The checked-in `docker-compose.yml` uses demonstration PostgreSQL credentials. **Replace the sample password and avoid publishing usable credentials before deploying or making this repository public.** Run PostgreSQL only in a trusted local environment.

```bash
docker compose up -d
```

### 3. Set environment variables

Create a local `.env` file (not committed to Git):

```dotenv
GCP_PROJECT_ID=your-own-gcp-project
GCP_LOCATION=us-central1
DB_HOST=localhost
DB_PORT=5432
DB_NAME=data_assistant
DB_USER=your-local-db-user
DB_PASSWORD=your-local-db-password
# Optional Langfuse configuration:
# LANGFUSE_PUBLIC_KEY=...
# LANGFUSE_SECRET_KEY=...
# LANGFUSE_HOST=https://cloud.langfuse.com
```

The DB values must match your local PostgreSQL configuration. Authenticate to your Google Cloud project with:

```bash
gcloud auth application-default login
```

### 4. Start the application

```bash
streamlit run app.py
```

## Using the App

### Synthetic Data Generation

1. Open **Data Generation**.
2. Upload a DDL file from `data/` or your own schema.
3. Optionally request a specific number of rows or other sample-data constraints.
4. Click **Generate**, inspect the tables, and download CSV/ZIP results.
5. If PostgreSQL is connected, generated tables can also be written to the database.

### Talk to Your Data

1. Load a schema and connect to PostgreSQL.
2. Navigate to **Talk to your data**.
3. Ask questions such as *"Which departments have the most employees?"*
4. Inspect the generated SQL, query results, and any generated visualization.

## Example Data

The `Synthetic_Data/` directory includes example CSV files for customers, companies, employees, restaurants, deliveries, and performance reviews. These are intended as sample datasets; inspect them before reuse.

## Concepts Demonstrated

- Structured generation grounded in database schema definitions.
- Prompt design and input validation for LLM applications.
- Translating natural language into executable SQL.
- DataFrame manipulation and relational database integration.
- Visualization and conversational analysis workflows.
- Responsible handling of untrusted model-generated code or queries.

## Limitations and Future Improvements

- Generated SQL should not be granted broad database permissions.
- Basic prompt-pattern checks do not stop all prompt injection or unsafe queries.
- Move all demonstration credentials out of tracked configuration and use a secrets manager for deployment.
- Improve schema validation, SQL parsing, execution limits, automated tests, and output verification.
- UI and generation require cloud credentials and external services; results may vary between model versions.

## Project Context

Adapted from a technical training project for portfolio documentation. Reuse or redistribution of training materials should follow the original project's permissions.

## Author

**Darius Costache** · [GitHub](https://github.com/Darius-Cos)
