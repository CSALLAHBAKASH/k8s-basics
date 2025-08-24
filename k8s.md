docker - build
kind - test
helm - deploy

minikube status
minikube start

pods are the smallest unit of compute

deployment scale and manage pods

service make pods discoverable

ingresses and ingress controllers make your app internet accessible

---

## Install docker

    sudo apt-get update -y
    sudo apt-get install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $USER # Add your user to the docker group to run docker without sudo
    newgrp docker # Apply the new group membership

## Install kind

    curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.22.0/kind-linux-amd64 # Replace v0.22.0 with the latest stable version from kind.sigs.k8s.io
    chmod +x ./kind
    sudo mv ./kind /usr/local/bin/kind

## Install kubectl

    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

## create cluster

    kind create cluster --name testcluster
    kind get clusters
    kind get kubeconfig --name testcluster
    kind get nodes --name testcluster

    kubectl cluster-info --context kind-testcluster
    kubectl get nodes

Kubernetes control plane is running at https://127.0.0.1:42287
CoreDNS is running at https://127.0.0.1:42287/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

### Deploy a sample app

    k run nginx --images nginx
    k get pods
    k get pods -o wide
    k describe pod nginx

    k explain pod
    k explain rc
    k explain rs

    k run redis --image=redis123 --dry-run=client -o yaml > redis.yaml
    k edit pod redis
    k apply -f redis.yaml

    k create -f rc-definition.yaml
    k create -f rs-definition.yaml

    <!-- scale -->
    k replace -f rs-definition.yaml
    k create -f rs-definition.yaml
    k scale  --replicas=3 -f rs-definition.yaml
    k scale  --replicas=1 replicaset nginx-rs
    k describe rc nginx-rc

    k scale  --replicas=3 -f rc-definition.yaml
    k scale  --replicas=1 replicationcontroller nginx-rc
    k describe rs nginx-rs

    k create -f deploy.yaml
    k get deploy

### update

    k apply -f deploy.yaml
    k set image deployment/myapp-deploy nginx=nginx:1.9.1

### status

    k rollout status deployment/app-deploy
    k rollout history deployment/app-deploy

### rollback

    k rollout undo deployment/app-deploy >> rollback >> k get rs (before and after)
    k create deployment app --image=httpd:2.4-alpine --replicas=3

### deployment strategy

    1. Recreate
    2. Rolling update(default)
        1. k apply -f deploy.yml
        2. k set image deployment/app nginx=nginx:1.9.1
    3. Blue-green

### rollback sequence

    k apply -f 04-deploy-definition.yaml
    k get deploy
    k rollout status deployment/nginx
    k delete deployment/nginx
    k apply -f 04-deploy-definition.yaml
    k rollout status deployment/nginx
    k rollout history deployment/nginx

    k apply -f 04-deploy-definition.yaml --record

    export KUBE_EDITOR="code --wait"
    k edit deploy nginx --record

## Networking

    Node ip : 192.168.1.2
    pod ip: 10.244.0.0/
        pod1: 10.244.02
        pod2: 10.244.03
        pod3: 10.244.04

    minikube service nginx --url
    k get nodes -o wide

## kubectl delete

    kubectl delete deployment my-deployment-1 my-deployment-2 service my-service-1
    kubectl delete deployment --all
    kubectl delete service --all
    kubectl delete deployment,service --all
    kubectl delete all --all -n <namespace-name>
    kubectl delete namespace <namespace-name>

## Testing with local setup images

    kind load docker-image app:v1 --name=testcluster
    k port-forward pod/app 8000:8000


    A Kubernetes Pod is not directly accessible from outside the cluster. The Pod's IP address is an internal IP that is only reachable by other Pods and nodes within the same cluster network. This is a fundamental concept of Kubernetes networking.

    To access your application from a browser, you need to expose your Pod using a Kubernetes Service. There are several types of services, each with a different method of exposure.

    1. The kubectl port-forward Method
        k run app --image=app:v1 --port 8000
        kubectl get pods
        kubectl port-forward pod/app-pod-name 8000:8000
        http://localhost:8080

    2. The NodePort Service Method
        kubectl expose pod app --type=NodePort --name=apps --port=8000 --target-port=8000
        kubectl get services my-app-service
        kubectl get nodes -o wide

        Access your application: Use the node's IP address and the assigned NodePort in your browser. The URL will look like http://<node-ip>:<nodeport>.

        For example: http://192.168.1.100:30001

    3. The LoadBalancer Service Method
        kubectl expose pod <your-pod-name> --type=LoadBalancer --name=my-app-service --port=8000 --target-port=8000
        kubectl get services my-app-service
