from airflow import DAG
from datetime import datetime
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator


def make_dbt_task(task_id: str, dbt_command: list[str]):
    return KubernetesPodOperator(
        task_id=task_id,
        name=task_id,
        namespace="dbt",
        service_account_name="airflow",
        image="my-dags:0.0.1",
        cmds=["dbt"],
        arguments=dbt_command + ["--profiles-dir", ".", "--target", "prod"],
        get_logs=True,
        is_delete_operator_pod=False,
        in_cluster=False,
        env_from=[{"secretRef": {"name": "postgres-db-connection"}}]
    )

with DAG(
    dag_id="dbt",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
):

    dbt_seed = make_dbt_task("dbt-seed", ["seed"])
    dbt_run = make_dbt_task("dbt-run", ["run"])
    dbt_test = make_dbt_task("dbt-test", ["test"])

    dbt_seed >> dbt_run >> dbt_test