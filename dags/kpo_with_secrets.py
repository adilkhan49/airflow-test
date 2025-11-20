from airflow import DAG
from datetime import datetime
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.kubernetes.secret import Secret

database_user = Secret(
   deploy_type="env", deploy_target="SECRET_1", secret="postgres-db-connection", key="database_user"
)

database_password = Secret(
   deploy_type="env", deploy_target="SECRET_1", secret="postgres-db-connection", key="database_password"
)

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
        image="busybox",
        cmds=["sh", "-c"],
        arguments=["echo $database_user $database_password "],
        get_logs=True,
        env_from=[{"secretRef": {"name": "postgres-db-connection"}}]
    )
