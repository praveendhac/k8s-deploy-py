# k8s_deploy
Kubernetes deployment using Python Kubernetes API

## Problem
Use Kubernetes library for Python to deploy and check a basic application (of our choice) onto a Kubernetes cluster (we can use Minikube or a cloud service for testing/demoing). 
This application should deploy at least a pod/deployment and a configMap/secret.

## Prerequisites
- python 3.x
- kubectl
- minikube/kubernetes cluster

## Environment
```
$ virtualenv --version
$ mkdir vir-env
$ virtualenv vir-env/k8s-deploy
$ cd vir-env/k8s-deploy/bin/
$ source activate
$ which python
/Users/pd/REPOS/PRAVEENDHAC/k8s_deploy.py/vir-env/k8s-deploy/bin/python
$ pip3 install requirements.txt
```

## Usage
### Create Deployment
Create Configmap before creating deployment
```
$ python src/k8s_deploy.py create deployment -n aidt-deployment -i nginx:1.14.2 --namespace aidt --label adit-nginx
create sys.argv: ['src/k8s_deploy.py', 'create', 'deployment', '-n', 'aidt-deployment', '-i', 'nginx:1.14.2', '--namespace', 'aidt']
deployment sys.argv: ['src/k8s_deploy.py', 'create', 'deployment', '-n', 'aidt-deployment', '-i', 'nginx:1.14.2', '--namespace', 'aidt']
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

python src/k8s_deploy.py create deployment -n test1-deployment -i nginx:1.14.2 --namespace test1 --cfgmapname test1-configmap --label pd-nginx
```
### Delete Deployment
```
$ python src/k8s_deploy.py delete deployment -n aidt-deployment --namespace aidt
Delete k8s Resources
deployment sys.argv: ['src/k8s_deploy.py', 'delete', 'deployment', '-n', 'aidt-deployment', '--namespace', 'aidt']
Using kubeconfig file from default location
Deleting deployment
Deployment deleted. status='{'observedGeneration': 1, 'replicas': 3, 'updatedReplicas': 3, 'readyReplicas': 3, 'availableReplicas': 3, 'conditions': [{'type': 'Available', 'status': 'True', 'lastUpdateTime': '2019-02-03T05:15:16Z', 'lastTransitionTime': '2019-02-03T05:15:16Z', 'reason': 'MinimumReplicasAvailable', 'message': 'Deployment has minimum availability.'}, {'type': 'Progressing', 'status': 'True', 'lastUpdateTime': '2019-02-03T05:15:16Z', 'lastTransitionTime': '2019-02-03T05:14:59Z', 'reason': 'NewReplicaSetAvailable', 'message': 'ReplicaSet "aidt-deployment-56cf96b4fd" has successfully progressed.'}]}'
```
### Create ConfigMap
```
$ python src/k8s_deploy.py create configmap -n pd-aidt-configmap --namespace aidt --config-file config/pd-config.json
create sys.argv: ['src/k8s_deploy.py', 'create', 'configmap', '-n', 'pd-aidt-configmap', '--namespace', 'aidt', '--config-file', 'config/pd-config.json']
Using kubeconfig file from default location
Configure ConfigMap metadata
config filename for configmap: config/pd-config.json
Creating Configmap
ConfigMap created status='{'api_version': 'v1',
 'binary_data': None,
 'data': {'config.json': '{\n'
                         "  'fname': 'Praveen',\n"
                         "  'lname': 'D',\n"
                         "  'profession': 'Security Architect',\n"
                         "  'description': 'Passionate Information Security "
                         "Professional'\n"
                         '}\n'},
 'kind': 'ConfigMap',
 'metadata': {'annotations': {'app': 'pd-aidt-test', 'person': 'praveend'},
              'cluster_name': None,
              'creation_timestamp': datetime.datetime(2019, 2, 4, 22, 25, 14, tzinfo=tzutc()),
              'deletion_grace_period_seconds': None,
              'deletion_timestamp': None,
              'finalizers': None,
              'generate_name': None,
              'generation': None,
              'initializers': None,
              'labels': {'app': 'pd-aidt-test', 'person': 'praveend'},
              'name': 'pd-aidt-configmap',
              'namespace': 'aidt',
              'owner_references': None,
              'resource_version': '535901',
              'self_link': '/api/v1/namespaces/aidt/configmaps/pd-aidt-configmap',
              'uid': 'be2a9492-28cb-11e9-b82d-080027d6d630'}}'
```

### Create Secret
```
$ python src/k8s_deploy.py create secret -n pd-opaq-secret --namespace aidt --secret-type opaque
create sys.argv: ['src/k8s_deploy.py', 'create', 'secret', '-n', 'pd-opaq-secret', '--namespace', 'aidt', '--secret-type', 'opaque']
Using kubeconfig file from default location
Creating Secret
{'api_version': 'v1',
 'data': {'authn': 'cHJhdmVlbjpEYXJzaGFuYW0xMVMzY3JldA==',
          'password': 'RGFyc2hhbmFtMTFTM2NyZXQ=',
          'token': 'MTEtMjItMzMtNDQ=',
          'username': 'cHJhdmVlbg=='},
 'kind': 'Secret',
 'metadata': {'annotations': None,
....
```

### Create Service
```
$ src/k8s_deploy.py create service -n nginx-svc-pd --namespace aidt ---protocol TCP --target-port 80 --port 80 --label nginx
```

### Check Status
```
$ kubectl get deployments -n aidt
NAME              DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
aidt-deployment   3         3         3            0           5s

$ kubectl get po -n aidt
NAME                               READY   STATUS    RESTARTS   AGE
aidt-deployment-56cf96b4fd-5d2wx   1/1     Running   0          20s
aidt-deployment-56cf96b4fd-6qbn6   1/1     Running   0          20s
aidt-deployment-56cf96b4fd-vrwvb   1/1     Running   0          20s

$ kubectl get secret -n aidt
NAME                  TYPE                                  DATA   AGE
default-token-vrwzr   kubernetes.io/service-account-token   3      1d
dpr-secret            kubernetes.io/dockerconfigjson        1      1d
pd-opaq-secret        opaque                                4      44s
```

### Access application
```
$ kubectl -n aidt port-forward pod/aidt-deployment-6fb7d76557-5kmww 8888:80
Forwarding from 127.0.0.1:8888 -> 80
Forwarding from [::1]:8888 -> 80
Handling connection for 8888
Handling connection for 8888
```

## Testing
```
cd test
python3 -m pytest k8s-deploy-unittest.py        # or py.test -v
```
## References
- https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md
- https://click.palletsprojects.com/en/7.x/ 
