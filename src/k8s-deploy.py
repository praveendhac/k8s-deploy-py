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
    pass

def initialize(kubeconfig):
  setClusterContext(kubeconfig)
  #v1 = k8s.client.CoreV1Api()
  v1 = k8s.client.AppsV1Api()
  return v1

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
    click.echo('Exception when calling create_namespaced_deployment')
    click.echo('EXCEPTION: %s' % e)
    return
  print("Deployment created. status='%s'" % str(api_response.status))

def update_deployment(v1_api, deployment, dep_name, new_image, ns):
  '''Update deployment'''
  click.echo('Update container image')
  deployment.spec.template.spec.containers[0].image = new_image
  click.echo('Update the deployment')
  api_response = v1_api.patch_namespaced_deployment(
    name=dep_name,
    namespace=ns,
    body=deployment)
  print("Deployment updated. status='%s'" % str(api_response.status))

@click.command()
@click.option('--name', '-n',help='k8s deployment name')
@click.option('--namespace', help='namespace for deployment')
def delete_deployment(v1_api, dname, ns):
  '''Delete deployment'''
  click.echo('Deleting deployment')
  api_response = v1_api.delete_namespaced_deployment(
    name=dname,
    namespace=ns,
    body=k8s.client.V1DeleteOptions(
      propagation_policy='Foreground',
      grace_period_seconds=5))
  print("Deployment deleted. status='%s'" % str(api_response.status))

@click.group()
#@click.command()
@click.option('--name', '-n',help='k8s deployment name')
@click.option('--image','-i',help='docker image to use')
@click.option('--namespace', help='namespace for deployment')
@click.option('--kube-config', '-k', type=click.File('r'), help='kubeconfig file')
def deployment(name, image, namespace, kube_config):
  '''Deployment operations'''
  v1 = initialize(kube_config)
  deployment = create_deployment_object(name, image)

  if not namespace:
    namespace = "default"
  create_deployment(v1, deployment, namespace)

  update_deployment(v1, deployment, name, image, namespace)

  delete_deployment(v1, name, namespace)

@click.command()
def configmap():
  click.echo('Configmap....')

@click.command()
def secret():
  click.echo('secret....')

@click.command()
@click.option('--set-context', nargs = 0, help='set cluster context')
@click.option('--get-context', nargs = 0, help='get cluster context')
@click.option('--kube-config', '-k', type=click.File('r'), help='kubeconfig file')
def cluster(name,image):
  click.echo('cluster....')
  print("sys.arg", sys.argv)
  click.echo('sc=%s' % set_context)
  click.echo('gc=%s' % get_context)
  
cli.add_command(deployment)
cli.add_command(configmap)
cli.add_command(secret)
cli.add_command(cluster)
deployment.add_command(create)
deployment.add_command(update)
deployment.add_command(delete)

def setClusterContext(kubeconfig):
  '''Loads authentication and cluster information from kube-config file'''
  if kubeconfig:
    click.echo('Using kubeconfig file: %s' % kubeconfig)
    k8s.config.load_kube_config(config_file=kubeconfig)
  else:
    k8s.config.load_kube_config(config_file=None)

def getClusterContext(kubeconfig):
  click.echo('%s',k8s.config.list_kube_config_contexts())

if __name__ == '__main__':
  cli()
