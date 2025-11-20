helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
helm repo update
helm uninstall kubernetes-dashboard -n kubernetes-dashboard
kubeclt delete namespacee kubernetes-dashboard
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard --wait
kubectl apply -f dashboard/dashboard-user.yml
kubectl apply -f dashboard/dashboard-user-config.yml

# pbcopy copies straight to clipboard
kubectl -n kubernetes-dashboard create token admin-user | pbcopy
kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443