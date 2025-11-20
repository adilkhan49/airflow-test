export NAMESPACE=airflow
export RELEASE_NAME=airflow

helm repo add apache-airflow https://airflow.apache.org
helm repo update
kubectl create namespace airflow
helm upgrade --install $RELEASE_NAME apache-airflow/airflow --set postgresql.image.tag=latest -f airflow/values.yaml -n $NAMESPACE
kubectl port-forward svc/$RELEASE_NAME-api-server 8080:8080 -n $NAMESPACE
