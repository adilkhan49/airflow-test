from airflow import DAG
from datetime import datetime
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator


with DAG(
    dag_id="dbt",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
):

    dbt_test = KubernetesPodOperator(
        task_id="dbt-test",
        name="dbt-test",
        namespace="airflow",
        image="my-dags:latest",
        cmds=["dbt"],
        arguments=["run", "--profiles-dir", "."],
        ## no change on below
        get_logs=True,
        is_delete_operator_pod=False,
        in_cluster=False,
        env_from=[{"secretRef": {"name": "postgres-db-connection"}}]
        )