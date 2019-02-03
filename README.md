# k8s-deploy-py
Kubernetes deployment using k8s Python API

## Problem
Use Kubernetes library for Python to deploy and check a basic application (of our choice) onto a Kubernetes cluster (we can use Minikube or a cloud service for testing/demoing). 
This application should deploy at least a pod/deployment and a configMap/secret.

## Usage
- Create Deployment
```
$ python src/k8s-deploy.py create deployment -n aidt-deployment -i nginx:1.14.2 --namespace aidt
create sys.argv: ['src/k8s-deploy.py', 'create', 'deployment', '-n', 'aidt-deployment', '-i', 'nginx:1.14.2', '--namespace', 'aidt']
deployment sys.argv: ['src/k8s-deploy.py', 'create', 'deployment', '-n', 'aidt-deployment', '-i', 'nginx:1.14.2', '--namespace', 'aidt']
Using kubeconfig file from default location
Create deployement
Deployment created. status='{'available_replicas': None,
 'collision_count': None,
 'conditions': None,
 'observed_generation': None,
 'ready_replicas': None,
 'replicas': None,
 'unavailable_replicas': None,
 'updated_replicas': None}'
```
- Delete Deployment
```
$ python src/k8s-deploy.py delete deployment -n aidt-deployment --namespace aidt
Delete k8s Resources
deployment sys.argv: ['src/k8s-deploy.py', 'delete', 'deployment', '-n', 'aidt-deployment', '--namespace', 'aidt']
Using kubeconfig file from default location
Deleting deployment
Deployment deleted. status='{'observedGeneration': 1, 'replicas': 3, 'updatedReplicas': 3, 'readyReplicas': 3, 'availableReplicas': 3, 'conditions': [{'type': 'Available', 'status': 'True', 'lastUpdateTime': '2019-02-03T05:15:16Z', 'lastTransitionTime': '2019-02-03T05:15:16Z', 'reason': 'MinimumReplicasAvailable', 'message': 'Deployment has minimum availability.'}, {'type': 'Progressing', 'status': 'True', 'lastUpdateTime': '2019-02-03T05:15:16Z', 'lastTransitionTime': '2019-02-03T05:14:59Z', 'reason': 'NewReplicaSetAvailable', 'message': 'ReplicaSet "aidt-deployment-56cf96b4fd" has successfully progressed.'}]}'
```
- Check Status
```
$ kubectl get deployments -n aidt
NAME              DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
aidt-deployment   3         3         3            0           5s

$ kubectl get po -n aidt
NAME                               READY   STATUS    RESTARTS   AGE
aidt-deployment-56cf96b4fd-5d2wx   1/1     Running   0          20s
aidt-deployment-56cf96b4fd-6qbn6   1/1     Running   0          20s
aidt-deployment-56cf96b4fd-vrwvb   1/1     Running   0          20s
```

## References
- https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md
- 
