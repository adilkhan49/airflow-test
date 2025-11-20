from airflow import DAG
from datetime import datetime
from airflow.contrib.kubernetes.secret import Secret
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

database_user = Secret(
   deploy_type="env", deploy_target="SECRET_1", secret="postgres-db-connection", key="database_user"
)

database_password = Secret(
   deploy_type="env", deploy_target="SECRET_1", secret="postgres-db-connection", key="database_password"
)

with DAG(
    dag_id="hello_k8s_pod",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
):

    hello = KubernetesPodOperator(
        task_id="hello-secret",
        name="hello-world",
        namespace="airflow",
        image="busybox",
        cmds=["sh", "-c"],
        arguments=["echo $database_user $database_password "],
        get_logs=True,
        secrets = [database_user,database_password]
    )
