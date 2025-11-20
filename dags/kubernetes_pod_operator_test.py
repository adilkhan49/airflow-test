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
        namespace="airflow",
        image="busybox",
        cmds=["sh", "-c"],
        arguments=["echo 'Hello from Kubernetes!'"],
        get_logs=True,
    )

    sleep = KubernetesPodOperator(
        task_id="sleep",
        name="sleep",
        namespace="airflow",
        image="busybox",
        cmds=["sh", "-c"],
        arguments=["sleep 60"],
        get_logs=True,
    )

    goodbye = KubernetesPodOperator(
        task_id="goodbye",
        name="goodbye",
        namespace="airflow",
        image="busybox",
        cmds=["sh", "-c"],
        arguments=["echo 'Goodbye!'"],
        get_logs=True,
    )

    hello >> sleep >> goodbye
