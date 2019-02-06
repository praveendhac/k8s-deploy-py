#!/usr/bin/env python3

import sys
import os
import click

sys.path.append(os.path.abspath('../src/'))
k8sdeploy = __import__("k8s_deploy")

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

def getCoreV1Api():
  k8s.config.load_kube_config()
  corev1api = k8s.client.CoreV1Api()
  return corev1api 

#def setClusterContext(kubeconfig):
#  '''Loads authentication and cluster information from kube-config file'''
#  if kubeconfig:
#    click.echo('Using kubeconfig file: %s' % kubeconfig)
#    k8s.config.load_kube_config(config_file=kubeconfig)
#  else:
#    click.echo('Using kubeconfig file from default location')
#    k8s.config.load_kube_config(config_file=None)
#
#def initializeCoreV1Api(kubeconfig):
#  setClusterContext(kubeconfig)
#  corev1api = k8s.client.CoreV1Api()
#  return corev1api

def test_get_all_namespaces():
  corev1api = getCoreV1Api()
  print("Testcase: get_all_namespaces")
  try: 
    api_response = corev1api.list_namespace()
  except ApiException as e:
    print("Exception when calling CoreV1Api->list_namespace: %s\n" % e)
  print("ns:", api_response)

test_get_all_namespaces()

def test_api_server():
  '''successfully get API server'''
  print("Testcase: api_server")
  corev1api = getCoreV1Api()
  print(__name__)
test_api_server()

def test_api_v1():
  '''basic check'''
  print("Testcase: api_v1")
  corev1api = getCoreV1Api()
  try:
    api_resp = corev1api.get_api_resources()
  except ApiException as e:
    print("Exception when calling CoreV1Api->get_api_resources: %s\n" % e)
  print(__name__, "api_v1:", api_resp)

test_api_v1()
  
def test_is_rbac_enabled():
  '''RBAC check'''
  print("Testcase: is_rbac_enabled")
  corev1api = getCoreV1Api()

def test_check_nodes():
  '''check node'''
  print("Testcase: check_nodes")
  corev1api = getCoreV1Api()
  try:
    ret = corev1api.list_node()
    print(ret)
  except ApiException as e:
    print("Exception when calling CoreV1Api->list_node: %s\n" % e)

test_check_nodes()

def test_check_node_pressures():
  '''check node pressure'''
  print("Testcase: check_node_pressures")
  corev1api = getCoreV1Api()

def test_check_control_plane():
  '''all control plane pods'''
  print("Testcase: check_control_plane")
  corev1api = getCoreV1Api()

def test_check_etcd():
  '''check etcd pod'''
  print("Testcase: check_etcd")
  corev1api = getCoreV1Api()

def test_check_pods():
  '''all pods in all namespaces'''
  print("Testcase: check_pods")
  corev1api = getCoreV1Api()
  ret = corev1api.list_pod_for_all_namespaces(watch=False)
  for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

test_check_pods()

def test_check_deployments():
  '''check deployments'''
  print("Testcase: check_deployments")
  corev1api = getCoreV1Api()

def test_check_services():
  '''check services'''
  print("Testcase: check_services")
  corev1api = getCoreV1Api()
  list_service_for_all_namespaces()

def test_check_secrets():
  '''check secrets'''
  print("Testcase: check_secrets")
  corev1api = getCoreV1Api()
  list_secret_for_all_namespaces()

def test_check_service_rechability():
  '''port-forward'''
  print("Testcase: check_service_rechability")
  corev1api = getCoreV1Api()

def test_detect_nonrunning_pods():
  '''pods not running'''
  print("Testcase: detect_nonrunning_pods")
  corev1api = getCoreV1Api()

def test_check_configmap_allns():
  print("Testcase: check_configmap_allns")
  corev1api = getCoreV1Api()
  list_config_map_for_all_namespaces()
