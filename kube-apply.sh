eval $(minikube docker-env)

docker build Users/ -t users

kubectl apply -Rf kubernates/
