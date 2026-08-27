Operations Data Quality Pipeline



A production-style Python data pipeline that ingests operational request data, normalizes correctable inconsistencies, validates business rules, quarantines invalid records, persists clean data to PostgreSQL, and generates SQL-backed operational analytics.

The project models a realistic internal-operations workflow where incoming data must be checked and cleaned before it can safely support reporting or downstream systems.

Features

Ingests operational request data from CSV files

Normalizes known status inconsistencies before validation

Detects missing values, duplicate request IDs, invalid categories, malformed dates, and invalid date sequences

Quarantines invalid records while preserving detected quality reasons

Persists validated records to SQLite or PostgreSQL

Generates operational metrics using SQL

Produces dataset-level data-quality metrics

Generates reproducible synthetic datasets with 10,000 records

Supports command-line input selection

Runs PostgreSQL and the Python pipeline with Docker Compose

Uses automated unit tests and GitHub Actions continuous integration

Architecture

                         Raw CSV Data
                              |
                              v
                         Data Ingestion
                              |
                              v
                         Normalization
                              |
                              v
                          Validation
                              |
                              v
                        Classification
                         /           \
                        /             \
                       v               v
              Valid Records      Quarantined Records
                   |              + Quality Reasons
                   v
              PostgreSQL
                   |
                   v
               SQL Analytics
                   |
                   v
          Operational Metrics

The pipeline separates correctable inconsistencies from records that cannot safely proceed. Known variations are normalized automatically, while records that violate validation rules are quarantined for investigation.

Technology Stack

Technology

Purpose

Python 3.13

Pipeline orchestration and application logic

Pandas

Data ingestion, transformation, validation, and reporting

SQL

Operational analytics and database queries

SQLite

Lightweight local database development and testing

PostgreSQL

Production-style relational data persistence

psycopg

Python/PostgreSQL connectivity

Docker

Application and database containerization

Docker Compose

Multi-container orchestration

unittest

Automated unit testing

GitHub Actions

Continuous integration

Git / GitHub

Version control and project hosting

Data Quality Checks

The validation layer currently checks for:

Check

Purpose

Required schema

Detect missing required columns

Required values

Detect incomplete records

Duplicate request IDs

Prevent duplicate operational requests

Department validation

Reject unsupported departments

Priority validation

Reject unsupported priority values

Status validation

Detect unsupported workflow statuses

Date validation

Detect malformed dates

Date-order validation

Prevent completion dates preceding submission dates

Known status variations are normalized before validation. For example, correctable values such as OPEN can be standardized to Open instead of unnecessarily quarantining the record.

Project Structure

operations-data-quality-pipeline/
|
|-- .github/
|   `-- workflows/
|       `-- tests.yml
|
|-- data/
|   |-- raw/
|   `-- processed/
|
|-- src/
|   |-- analytics.py
|   |-- classifiers.py
|   |-- config.py
|   |-- database.py
|   |-- generator.py
|   |-- pipeline.py
|   |-- quality_metrics.py
|   |-- transformers.py
|   |-- validators.py
|   `-- writers.py
|
|-- tests/
|
|-- .dockerignore
|-- .env.example
|-- .gitignore
|-- Dockerfile
|-- docker-compose.yml
|-- requirements.txt
`-- README.md

Generated databases, processed datasets, large synthetic datasets, and local environment configuration are intentionally excluded from version control.

Getting Started

Clone the repository

git clone https://github.com/dbridgelall/operations-data-quality-pipeline.git
cd operations-data-quality-pipeline

Local Python setup

Create a virtual environment:

python -m venv .venv

Activate it on Windows PowerShell:

.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Run the included sample dataset:

python -m src.pipeline

Generate a larger demonstration dataset

python -m src.generator

The generator creates a reproducible synthetic operational dataset containing 10,000 records with intentionally injected data-quality problems.

Process the generated dataset with:

python -m src.pipeline --input data/raw/generated_operations_requests.csv

Running with Docker

Copy the example environment configuration:

cp .env.example .env

On Windows PowerShell:

Copy-Item .env.example .env

Update the local PostgreSQL password in .env, then build and start the services:

docker compose up --build

Docker Compose starts PostgreSQL, waits for the database health check to pass, and then executes the Python pipeline. The pipeline container exits after processing completes, while PostgreSQL remains available for queries.

To stop the environment:

docker compose down

Testing

Run the complete test suite:

python -m unittest discover -v

The automated test suite covers transformations, validation, classification, persistence, SQL analytics, configuration, synthetic data generation, output handling, and data-quality metrics.

GitHub Actions automatically executes the test suite for pushes and pull requests targeting main.

Example 10,000-Record Run

The synthetic data generator can exercise the pipeline at a larger scale while preserving reproducibility.

Verified example output:

Total records: 10,000
Valid records: 9,920
Quarantined records: 80
Quality rate: 99.20%
Detected record-level issues: 80

The generated benchmark contained 20 missing required values, 20 invalid departments, 20 invalid priorities, and 20 malformed dates. Known status variations were normalized before validation and therefore did not require quarantine.

Because validation issues can overlap on the same record, the number of detected issues can differ from the number of quarantined records in other generated datasets.

Design Decisions

Normalize before rejecting

Correctable inconsistencies are normalized before validation. Records are quarantined only when the pipeline cannot safely resolve the underlying issue.

Preserve rejection reasons

A record can violate multiple quality rules. Quarantined records retain detected quality issues so failures can be investigated instead of silently discarded.

Separate pipeline responsibilities

Ingestion, transformation, validation, classification, persistence, analytics, and reporting are implemented as separate reusable components instead of one large pipeline function.

Support multiple relational databases

SQLite provides lightweight local development and isolated testing, while PostgreSQL provides a more production-oriented persistence layer. Database-specific SQL is handled explicitly where the dialects differ.

Keep generated artifacts out of version control

Processed CSV files, generated databases, large synthetic datasets, and local credentials are reproducible runtime artifacts and are excluded from Git.