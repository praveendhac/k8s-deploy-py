#!/usr/bin/env python3

import sys
import os
import click

#sys.path.append('../src')
sys.path.append(os.path.abspath('../src/'))
#import k8s-deploy
k8sdeploy = __import__("k8s-deploy")

try:
  import kubernetes as k8s
  from kubernetes.client.rest import ApiException
except ImportError:
  print("kubernetes package not installed, run \"pip3 install kubernetes\"")
  sys.exit(-1)

try:
  import pytest
except ImportError:
  print("kubernetes package not installed, run \"pip3 install pytest\"")
  sys.exit(-1)

def setClusterContext(kubeconfig):
  '''Loads authentication and cluster information from kube-config file'''
  if kubeconfig:
    click.echo('Using kubeconfig file: %s' % kubeconfig)
    k8s.config.load_kube_config(config_file=kubeconfig)
  else:
    click.echo('Using kubeconfig file from default location')
    k8s.config.load_kube_config(config_file=None)

def initializeCoreV1Api(kubeconfig):
  setClusterContext(kubeconfig)
  corev1api = k8s.client.CoreV1Api()
  return corev1api

def test_get_namespaces():
  # set kubeconfig context using export KUBECONFIG for now
  kubeconfig = ""
  corev1api = initializeCoreV1Api(kubeconfig)
  try: 
    #api_response = corev1api.list_namespace(include_uninitialized=include_uninitialized, pretty=pretty, _continue=_continue, field_selector=field_selector, label_selector=label_selector, limit=limit, resource_version=resource_version, timeout_seconds=timeout_seconds, watch=watch)
    api_response = corev1api.list_namespace()
  except ApiException as e:
    print("Exception when calling CoreV1Api->list_namespace: %s\n" % e)
  print("ns:", api_response)

test_get_namespaces()

def api_server():
  '''successfully get API server'''

def api_v1():
  '''basic check'''

def is_rbac_enabled():
  '''RBAC check'''

def check_nodes():
  '''check node'''

def check_node_pressures():
  '''check node pressure'''

def check_control_plane():
  '''all control plane pods'''
def check_etcd():
  '''check etcd pod'''

def check_pods():
  '''all pos in all namespaces'''
  ''' or pod status'''

def check_deployments():
  '''check deployments'''

def check_services():
  '''check services'''

def check_service_rechability():
  '''port-forward'''

def detect_nonrunning_pods():
  '''pods not running'''


