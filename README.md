# DBT + Airflow on Kubernetes (Kind)

This project demonstrates running dbt jobs orchestrated by Airflow on a local Kubernetes cluster using **Kind**, with dbt credentials securely stored as Kubernetes secrets.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [Running DBT Tasks](#running-dbt-tasks)
- [Notes / Best Practices](#notes--best-practices)

---

## Prerequisites

Make sure you have the following installed locally:

- [Docker](https://www.docker.com/get-started)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Kind](https://kind.sigs.k8s.io/)
- [Airflow CLI / Docker image if needed](https://airflow.apache.org/docs/)

---

## Setup Instructions

### 1. Run a local Postgres database

```bash
docker run --name my-postgres -e POSTGRES_PASSWORD=my_password -d -p 5433:5432 postgres
```

This will start Postgres locally on port `5433` with password `my_password`.

---

### 2. Start a local Kubernetes cluster (Kind)

```bash
sh deploy-kind.sh
```

This script will create a Kind cluster configured for running Airflow and dbt pods.

---

### 3. Deploy Airflow onto the cluster

```bash
sh deploy-airflow.sh
```

This will deploy Airflow using Kubernetes resources or Helm charts, depending on your setup.

---

### 4. Add Postgres credentials as Kubernetes secrets

```bash
kubectl apply -f db-secrets.yaml
```

Secrets will be used by dbt jobs to connect to the database securely.

---

### 5. Build and load your dbt Docker image

```bash
docker build -t my-dags:0.0.1 .
kind load docker-image my-dags:0.0.1
```

This builds your dbt + DAG code image and loads it into the Kind cluster so it can be used by KubernetesPodOperator.

---

### 6. Prepare a dedicated namespace for dbt

```bash
kubectl create namespace dbt
kubectl create sa sa-dbt -n dbt
```

- Creates the `dbt` namespace to isolate dbt pods
- Creates a ServiceAccount `sa-dbt` for running dbt jobs
- You can attach Role and RoleBinding for RBAC if needed

---

## Project Structure

```
├── dags/                 # Airflow DAGs
├── dbt/                  # dbt project
│   ├── dbt_project.yml
│   ├── models/
│   └── profiles.yml      # Uses env_var() to load secrets
├── deploy-airflow.sh     # Script to deploy Airflow to Kind
├── deploy-kind.sh        # Script to create the Kind cluster
├── db-secrets.yaml       # Kubernetes secrets for Postgres
├── Dockerfile            # Builds dbt + DAGs image
└── README.md
```

---

## Running DBT Tasks

1. The DAGs in Airflow will run dbt tasks in the `dbt` namespace using the `sa-dbt` ServiceAccount.
2. dbt credentials are read from the Kubernetes secret via environment variables, injected into `profiles.yml` using `env_var()`.
3. Typical dbt workflow in Airflow:

```
dbt_seed → dbt_run → dbt_test
```

- Each step runs in its own Kubernetes pod via `KubernetesPodOperator`.

---

## Notes / Best Practices

- Always keep secrets in Kubernetes Secrets, **never in Git**.
- Set resource requests and limits for dbt pods to prevent cluster overload.
- Use `is_delete_operator_pod=True` in production to clean up pods automatically.
- Use separate namespaces for Airflow and dbt to isolate workloads.
- Tag Docker images with version or git commit hash for reproducibility.
- Consider using CI/CD to build images and deploy DAGs automatically.

---

This setup allows you to run a **fully local, isolated Airflow + dbt environment** on Kubernetes, with proper secrets management, RBAC, and containerized reproducibility.