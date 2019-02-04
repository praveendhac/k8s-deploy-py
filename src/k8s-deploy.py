#!/usr/bin/env python3
import sys

try:
  import kubernetes as k8s
  from kubernetes.client.rest import ApiException
except ImportError:
  print("kubernetes package not installed, run \"pip3 install kubernetes\"")

try:
  import click
except ImportError:
  print("click package not installed, run \"pip3 install click\"")

@click.group()
def cli():
  '''Manage Kubernetes(k8s) Resources'''
  pass

@click.group()
def create():
  '''Create k8s Resources'''    
  print("create sys.argv:", sys.argv)

@click.group()
def update():
  '''Update k8s Resources'''    
  click.echo('Update k8s Resources')

@click.group()
def delete():
  '''Delete k8s Resources'''    
  click.echo('Delete k8s Resources')

def setClusterContext(kubeconfig):
  '''Loads authentication and cluster information from kube-config file'''
  if kubeconfig:
    click.echo('Using kubeconfig file: %s' % kubeconfig)
    k8s.config.load_kube_config(config_file=kubeconfig)
  else:
    click.echo('Using kubeconfig file from default location')
    k8s.config.load_kube_config(config_file=None)

def getClusterContext(kubeconfig):
  click.echo('%s',k8s.config.list_kube_config_contexts())

def initializeAppsV1Api(kubeconfig):
  setClusterContext(kubeconfig)
  appsv1api = k8s.client.AppsV1Api()
  return appsv1api

def create_deployment_object(dname,image):
  # Configureate Pod template container
  container = k8s.client.V1Container(
    name="nginx",
    image=image,
    ports=[k8s.client.V1ContainerPort(container_port=80)],
    image_pull_policy="Always")
  # Create and configurate a spec section
  template = k8s.client.V1PodTemplateSpec(
    metadata= k8s.client.V1ObjectMeta(labels={"app": "nginx"}),
    spec=k8s.client.V1PodSpec(containers=[container]))
  # Create the specification of deployment
  spec = k8s.client.V1DeploymentSpec(
    replicas=3,
    template=template,
    selector=k8s.client.V1LabelSelector(match_labels={"app": "nginx"}))
  # Instantiate the deployment object
  deployment = k8s.client.V1Deployment(
    api_version="apps/v1",
    kind="Deployment",
    metadata= k8s.client.V1ObjectMeta(name=dname, labels={"app": "nginx"}),
    spec=spec)

  return deployment

def create_deployment(v1_api, deployment, ns):
  '''Create deployment'''
  click.echo('Create deployement')
  try:
    api_response = v1_api.create_namespaced_deployment(
      body=deployment,
      namespace=ns)
  except ApiException as e:
    click.echo('EXCEPTION: %s' % e)
    sys.exit(-1)
  print("Deployment created. status='%s'" % str(api_response.status))

def update_deployment(v1_api, deployment, dep_name, new_image, ns):
  '''Update deployment'''
  click.echo('Update container image deployment (%s)', deployment)
  deployment.spec.template.spec.containers[0].image = new_image
  click.echo('Updating the deployment')
  try:
    api_response = v1_api.patch_namespaced_deployment(
      name=dep_name,
      namespace=ns,
      body=deployment)
  except ApiException as e:
    click.echo('EXCEPTION: %s' % e)
    sys.exit(-1)

  print("Deployment updated. status='%s'" % str(api_response.status))

def delete_deployment(v1_api, dname, ns):
  '''Delete deployment'''
  click.echo('Deleting deployment')
  try:
    api_response = v1_api.delete_namespaced_deployment(
      name=dname,
      namespace=ns,
      body=k8s.client.V1DeleteOptions(
        propagation_policy='Foreground',
        grace_period_seconds=5))
  except ApiException as e:
    click.echo('EXCEPTION: %s' % e)
    sys.exit(-1)

  print("Deployment deleted. status='%s'" % str(api_response.status))

@click.command()
@click.option('--name', '-n',help='k8s deployment name')
@click.option('--image','-i',help='docker image to use')
@click.option('--namespace', help='namespace for deployment')
@click.option('--kube-config', '-k', type=click.File('r'), help='kubeconfig file')
def deployment(name, image, namespace, kube_config):
  print("deployment sys.argv:", sys.argv)
  '''Deployment operations'''
  v1 = initializeAppsV1Api(kube_config)
  deployment = create_deployment_object(name, image)

  if not namespace:
    namespace = "default"

  if sys.argv[1] == 'create':
    create_deployment(v1, deployment, namespace)
  elif sys.argv[1] == 'update':
    update_deployment(v1, deployment, name, image, namespace)
  elif sys.argv[1] == 'delete':
    delete_deployment(v1, name, namespace)
  else:
    click.echo('Unknown Command!')
    sys.exit(-1)

def initializeCoreV1Api(kubeconfig):
  setClusterContext(kubeconfig)
  corev1api = k8s.client.CoreV1Api()
  return corev1api

def create_configmap_object(cfg_map_name, cfg_map_file, ns):
  '''Create ConfigMap Object'''
  click.echo('Configure ConfigMap metadata')
  metadata = k8s.client.V1ObjectMeta(
    annotations=dict(app='pd-aidt-test', person='praveend'),
    deletion_grace_period_seconds=30,
    labels=dict(app='pd-aidt-test', person='praveend'),
    name=cfg_map_name,
    namespace=ns
  )

  # Get File Content for ConfigMap
  click.echo('config filename for configmap: %s' % cfg_map_file)
  with open(cfg_map_file, 'r') as cfgmap_fh:
    cfg_map_content = cfgmap_fh.read()

  # Instantiate configmap object
  configmap = k8s.client.V1ConfigMap(
    api_version="v1",
    kind="ConfigMap",
    data=dict(test=cfg_map_content),
    metadata=metadata
  )
  return configmap

def create_configmap(core_v1_api, configmap, name, ns):
  '''Create Configmap'''
  click.echo('Creating Configmap')
  try:
    api_response = core_v1_api.create_namespaced_config_map(
      namespace=ns, body=configmap)
  except ApiException as e:
    click.echo('EXCEPTION: %s' % e)
    sys.exit(-1)
  print("ConfigMap created status='%s'" % str(api_response))

def delete_configmap(name, namespace):
  '''Delete Configmap'''
  click.echo('Deleting Configmap')

@click.command()
@click.option('--name', '-n',help='k8s configmap name')
@click.option('--namespace', 'ns', help='namespace for configmap creation')
@click.option('--config-file', 'cnf_file', help='Configuration file')
@click.option('--kube-config', '-k', type=click.File('r'), help='kubeconfig file')
def configmap(name, ns, cnf_file, kube_config):
  '''Operations on Kubernetes ConfigMap Resource'''
  core_v1_api = initializeCoreV1Api(kube_config)
  configmap_obj = create_configmap_object(name, cnf_file, ns)

  if sys.argv[1] == "create":
    create_configmap(core_v1_api, configmap_obj, name, ns)
  elif sys.argv[1] == "delete":
    delete_configmap(name, ns)
  else:
    click.echo('Unknown Command!')
    sys.exit(-1)

def create_secret(core_v1_api, sname, ns, secret_type):
  '''Create Secret'''
  click.echo('Creating Secret')
  metadata = {'name': sname, 'namespace': ns}
  # secret data is key, value pairs when values is base64 encoded
  data = {'authn': 'cHJhdmVlbjpEYXJzaGFuYW0xMVMzY3JldA==', 'username': 'cHJhdmVlbg==',
          'password': 'RGFyc2hhbmFtMTFTM2NyZXQ=', 'token': 'MTEtMjItMzMtNDQ='}
  api_version = 'v1'
  kind = 'Secret'
  body = k8s.client.V1Secret(api_version, data, kind, metadata, 
    type=secret_type)
  try:
    api_response = core_v1_api.create_namespaced_secret(ns, body)
    click.echo(api_response)
  except ApiException as e:
    click.echo('EXCEPTION: %s' % e)
    sys.exit(-1)
  print("Deployment created. status='%s'" % str(api_response.status))

def delete_secret(core_v1_api, sname, ns):
  '''Delete Secret'''
  click.echo('Deleting Secret')

@click.command()
@click.option('--name', '-n',help='k8s secret name')
@click.option('--namespace', 'ns', help='namespace for secret creation')
@click.option('--secret-type', help='secret type(opaque, kubernetes.io/service-account-token, kubernetes.io/tls etc.)')
@click.option('--kube-config', '-k', type=click.File('r'), help='kubeconfig file')
def secret(name, ns, secret_type, kube_config):
  '''Operations on Kubernetes Secret Resource'''
  core_v1_api = initializeCoreV1Api(kube_config)

  if sys.argv[1] == "create":
    create_secret(core_v1_api, name, ns, secret_type)
  elif sys.argv[1] == "delete":
    delete_secret(core_v1_api, name, ns)
  else:
    click.echo('Unknown Command!')
    sys.exit(-1)

@click.command()
def pod():
  click.echo('secret....')

@click.command()
@click.option('--set-context', nargs = 0, help='set cluster context')
@click.option('--get-context', nargs = 0, help='get cluster context')
@click.option('--kube-config', '-k', type=click.File('r'), help='kubeconfig file')
def cluster(name,image):
  click.echo('cluster....')
  print("cluster sys.argv:", sys.argv)
  click.echo('sc=%s' % set_context)
  click.echo('gc=%s' % get_context)
  
cli.add_command(create)
cli.add_command(update)
cli.add_command(delete)

create.add_command(deployment)
create.add_command(configmap)
create.add_command(secret)
create.add_command(pod)

update.add_command(deployment)
update.add_command(configmap)
update.add_command(secret)
update.add_command(pod)

delete.add_command(deployment)
delete.add_command(configmap)
delete.add_command(secret)
delete.add_command(pod)

if __name__ == '__main__':
  cli()
