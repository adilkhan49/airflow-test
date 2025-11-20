FROM python:3.11-slim

RUN pip install --no-cache-dir dbt-core==1.10 dbt-postgres

WORKDIR /dbt

COPY dbt ./