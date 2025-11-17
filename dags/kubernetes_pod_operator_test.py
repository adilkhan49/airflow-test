from airflow import DAG
from datetime import datetime
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

with DAG(
    dag_id="hello_k8s_pod",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
):

    hello = KubernetesPodOperator(
        task_id="hello",
        name="hello-world",
        namespace="default",
        image="busybox",
        cmds=["sh", "-c"],
        arguments=["echo 'Hello from Kubernetes!'"],
        get_logs=True,
    )
