from airflow import DAG
from datetime import datetime
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator


with DAG(
    dag_id="hello_secrets",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
):

    hello = KubernetesPodOperator(
        task_id="hello-secret",
        name="hello-secret",
        namespace="airflow",
        image="alpine:3.19",
        cmds=["sh", "-c"],
        arguments=["echo $database_username $database_password"],
        get_logs=True,
        env_from=[{"secretRef": {"name": "postgres-db-connection"}}]
    )
