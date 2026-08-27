# Operations Data Quality Pipeline

[![Python Tests](https://github.com/dbridgelall/operations-data-quality-pipeline/actions/workflows/tests.yml/badge.svg)](https://github.com/dbridgelall/operations-data-quality-pipeline/actions/workflows/tests.yml)

A production-style **Python data pipeline** that ingests operational request data, normalizes correctable inconsistencies, validates business rules, quarantines invalid records, persists clean data to **SQLite or PostgreSQL**, and generates **SQL-backed operational analytics**.

The project models a realistic internal-operations workflow where incoming data must be checked and cleaned before it can safely support reporting or downstream systems.

---

## Key Features

- Ingests operational request data from CSV files
- Normalizes known data inconsistencies before validation
- Detects missing values, duplicate request IDs, invalid categories, malformed dates, and invalid date sequences
- Quarantines invalid records while preserving detected quality issues
- Persists validated records to **SQLite or PostgreSQL**
- Generates operational analytics using SQL
- Calculates dataset-level data-quality metrics
- Generates reproducible **10,000-record synthetic datasets**
- Supports command-line input selection
- Containerizes the Python pipeline and PostgreSQL with **Docker Compose**
- Includes automated unit testing
- Runs tests automatically through **GitHub Actions CI**

---

## Architecture

```text
                         Raw CSV Data
                              │
                              ▼
                       ┌─────────────┐
                       │  Ingestion  │
                       └──────┬──────┘
                              │
                              ▼
                       ┌─────────────┐
                       │Normalize Data│
                       └──────┬──────┘
                              │
                              ▼
                       ┌─────────────┐
                       │ Validation  │
                       └──────┬──────┘
                              │
                              ▼
                       ┌─────────────┐
                       │Classification│
                       └──────┬──────┘
                              │
                   ┌──────────┴──────────┐
                   │                     │
                   ▼                     ▼
          ┌────────────────┐    ┌─────────────────┐
          │ Valid Records  │    │   Quarantined   │
          └───────┬────────┘    │     Records     │
                  │             │ + Quality Issues│
                  │             └─────────────────┘
                  ▼
          ┌────────────────┐
          │ SQLite /       │
          │ PostgreSQL     │
          └───────┬────────┘
                  │
                  ▼
          ┌────────────────┐
          │ SQL Analytics  │
          └───────┬────────┘
                  │
                  ▼
          ┌────────────────┐
          │ Operational    │
          │ Metrics        │
          └────────────────┘
```

The pipeline follows a **normalize → validate → classify** approach. Correctable inconsistencies are standardized automatically, while records that cannot safely proceed are quarantined for investigation.

---

## Technology Stack

| Technology | Role in Project |
| --- | --- |
| **Python 3.13** | Pipeline orchestration and application logic |
| **Pandas** | CSV ingestion, transformations, validation, and reporting |
| **SQL** | Database queries and operational analytics |
| **SQLite** | Lightweight local development and isolated testing |
| **PostgreSQL** | Production-style relational data persistence |
| **psycopg** | Python-to-PostgreSQL connectivity |
| **Docker** | Application and database containerization |
| **Docker Compose** | Multi-container orchestration |
| **unittest** | Automated unit testing |
| **GitHub Actions** | Continuous integration |
| **Git / GitHub** | Version control and project hosting |

---

## Data Quality Validation

The validation layer checks incoming records before they are allowed into the validated dataset.

| Validation | What It Detects |
| --- | --- |
| Required schema | Missing required columns |
| Required values | Incomplete records |
| Duplicate request IDs | Duplicate operational requests |
| Department validation | Unsupported departments |
| Priority validation | Unsupported priority values |
| Status validation | Unsupported workflow statuses |
| Date validation | Missing or malformed date values |
| Date-order validation | Completion dates occurring before submission dates |

### Normalize Before Rejecting

Not every inconsistent value needs to be discarded.

For example:

```text
OPEN
```

can safely be normalized to:

```text
Open
```

before validation.

Records are quarantined only when the pipeline cannot safely resolve the underlying quality issue.

---

## Data Classification

After validation, records are separated into two outputs:

```text
Incoming Records
       │
       ▼
   Validation
       │
       ├──────── Valid ────────► valid_requests.csv
       │
       └──────── Invalid ──────► quarantined_requests.csv
                                      │
                                      └── quality_issues
```

Quarantined records retain their detected quality issues so problems can be investigated rather than silently discarded.

A single record can contain more than one issue.

---

## Verified 10,000-Record Benchmark

The project includes a reproducible synthetic data generator for exercising the pipeline at a larger scale.

A verified 10,000-record run produced:

| Metric | Result |
| --- | ---: |
| **Total Records** | **10,000** |
| **Valid Records** | **9,920** |
| **Quarantined Records** | **80** |
| **Quality Rate** | **99.20%** |
| **Detected Record-Level Issues** | **80** |

### Injected Quality Problems

| Problem | Records Detected |
| --- | ---: |
| Missing required values | 20 |
| Invalid departments | 20 |
| Invalid priorities | 20 |
| Malformed dates | 20 |
| Invalid statuses after normalization | 0 |

The generator also injects known status variations. Those values are corrected during normalization and therefore do not require quarantine.

Because multiple validation problems can occur on the same record, the number of detected issues may differ from the number of quarantined records in other generated datasets.

---

## Example Analytics

Validated records are persisted to a relational database and queried to produce operational metrics.

The verified 10,000-record run produced:

```text
Operational Analytics
---------------------
Total validated requests: 9,926
Average processing time: 5.1 days

Requests by Department
----------------------
Finance       2,045
IT            2,034
Facilities    1,994
HR            1,955
Operations    1,898

Requests by Status
------------------
Completed      3,359
In Progress    3,326
Open           3,241
```

> **Note:** The analytics database used for this run already contained records from previous pipeline executions, while the dataset-quality metrics describe the current 10,000-record input. The persistence layer uses upsert behavior rather than replacing the database with a snapshot on every run.

---

## Project Structure

```text
operations-data-quality-pipeline/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── analytics.py
│   ├── classifiers.py
│   ├── config.py
│   ├── database.py
│   ├── generator.py
│   ├── pipeline.py
│   ├── quality_metrics.py
│   ├── transformers.py
│   ├── validators.py
│   └── writers.py
│
├── tests/
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

Generated databases, processed datasets, large synthetic datasets, virtual environments, and local credentials are excluded from version control.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/dbridgelall/operations-data-quality-pipeline.git
cd operations-data-quality-pipeline
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Sample Pipeline

```bash
python -m src.pipeline
```

The included sample dataset intentionally contains multiple quality problems so the validation and quarantine workflow can be demonstrated.

---

## Generate a 10,000-Record Dataset

Generate the reproducible synthetic dataset:

```bash
python -m src.generator
```

The generated file is written to:

```text
data/raw/generated_operations_requests.csv
```

Process it with:

```bash
python -m src.pipeline --input data/raw/generated_operations_requests.csv
```

Generated datasets are intentionally excluded from Git because they can be reproduced at any time.

---

## Running with PostgreSQL and Docker

The project supports a fully containerized environment consisting of:

```text
             Docker Compose
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
   Python Pipeline       PostgreSQL
      Container           Container
          │                   ▲
          └───────────────────┘
```

### 1. Create Local Environment Configuration

Copy the example configuration:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Update the PostgreSQL password in `.env`.

> `.env` is excluded from Git so local database credentials are not committed to the repository.

### 2. Build and Start

```bash
docker compose up --build
```

Docker Compose will:

1. Build the Python pipeline image
2. Start PostgreSQL
3. Wait for the PostgreSQL health check
4. Start the Python pipeline
5. Connect the pipeline to PostgreSQL
6. Process and validate the sample dataset
7. Persist validated records
8. Generate SQL-backed analytics

The pipeline is a batch-processing application, so successful execution ends with:

```text
operations-pipeline exited with code 0
```

PostgreSQL remains available after the pipeline completes.

### 3. Stop the Environment

```bash
docker compose down
```

To also remove the development database volume:

```bash
docker compose down -v
```

---

## Testing

Run the complete automated test suite with:

```bash
python -m unittest discover -v
```

The test suite covers areas including:

- Data transformations
- Schema and record validation
- Record classification
- Database persistence
- SQL analytics
- Configuration
- Synthetic data generation
- Output handling
- Data-quality metrics

---

## Continuous Integration

GitHub Actions automatically creates a clean environment, installs the project's dependencies, and executes the complete test suite for:

```text
Push to main
      │
      ▼
GitHub Actions
      │
      ▼
Python 3.13
      │
      ▼
Install Dependencies
      │
      ▼
Run Unit Tests
      │
      ▼
   PASS / FAIL
```

The workflow runs automatically on:

- Pushes to `main`
- Pull requests targeting `main`

This helps catch regressions before new code is incorporated into the project.

---

## Design Decisions

### Modular Pipeline Architecture

Ingestion, transformation, validation, classification, persistence, analytics, and reporting are separated into reusable modules rather than implemented as one large function.

### Preserve Rejected Data

Invalid records are quarantined instead of deleted. This preserves the original data and associated quality issues for investigation.

### Normalize Correctable Values

Known inconsistencies are corrected before validation when they can be resolved safely.

### Multiple Database Backends

SQLite provides lightweight local development and isolated testing, while PostgreSQL provides a more production-oriented relational database environment.

### Reproducible Synthetic Data

The synthetic generator uses a fixed random seed so benchmark datasets can be recreated consistently.

### Containerized Execution

Docker separates the application's runtime environment from the developer's local machine, while Docker Compose coordinates the pipeline and PostgreSQL services.

### Automated Verification

Unit tests and GitHub Actions provide repeatable checks that changes have not broken existing behavior.

---

## Skills Demonstrated

This project demonstrates practical experience with:

**Python • Pandas • SQL • PostgreSQL • SQLite • Docker • Docker Compose • GitHub Actions • CI • Git • GitHub • Unit Testing • Data Validation • ETL/Data Pipelines • Data Quality • Relational Databases • CLI Development**

---

## Future Improvements

Potential extensions include:

- Structured application logging
- Configurable validation rules
- Database migration tooling
- Pipeline execution statistics
- Additional data-quality dimensions
- Scheduled pipeline execution
- REST API or dashboard for reviewing quarantined records

---

## Project Status

**Core pipeline complete.**

The current implementation supports data ingestion, normalization, validation, quarantine handling, quality measurement, relational persistence, SQL analytics, synthetic dataset generation, automated testing, continuous integration, and containerized execution.