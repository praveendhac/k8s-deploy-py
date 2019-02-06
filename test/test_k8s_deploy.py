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

def getCoreApi():
  k8s.config.load_kube_config()
  coreapi = k8s.client.CoreApi()
  return coreapi

def getRbacAuthorizationApi():
  k8s.config.load_kube_config()
  rbacauthorizationapi = k8s.client.RbacAuthorizationV1Api()
  return rbacauthorizationapi

def test_get_all_namespaces():
  ns = []
  corev1api = getCoreV1Api()
  print("Testcase: get_all_namespaces")
  try: 
    api_response = corev1api.list_namespace()
  except ApiException as e:
    print("Exception when calling CoreV1Api->list_namespace: %s\n" % e)
  resp_dict = api_response.to_dict()
  for item in resp_dict['items']:
    metadata = item['metadata']
    # add all the namespaces in the cluster to ns list
    ns.append(metadata['name'])
  print("ns:", ns)
  assert len(ns) >= 3

def test_api_server():
  '''successfully get API server'''
  print("Testcase: api_server")
  coreapi = getCoreApi()
  resp = coreapi.get_api_versions().to_dict()
  # Kubernetes API Server IP:Port or domain:port
  api_server = resp['server_address_by_client_cid_rs'][0]['server_address']
  # checks api_server is not empty
  assert api_server

def test_api_v1_resources():
  '''basic check'''
  print("Testcase: api_v1")
  corev1api = getCoreV1Api()
  try:
    api_resp = corev1api.get_api_resources().to_dict()
  except ApiException as e:
    print("Exception when calling CoreV1Api->get_api_resources: %s\n" % e)
  # totak k8s resources for v1 API
  total_k8s_v1_api_resources = len(api_resp['resources'])
  print("Total k8s v1_api resources:", total_k8s_v1_api_resources)
  assert total_k8s_v1_api_resources > 1
  
def test_is_rbac_enabled():
  '''RBAC check'''
  print("Testcase: is_rbac_enabled")
  rbacauthorizationapi = getRbacAuthorizationApi()
  #resp = rbacauthorizationapi.get_api_group().to_dict()
  resp = rbacauthorizationapi.get_api_resources().to_dict()
  print("resp:", resp)
test_is_rbac_enabled()

def test_check_nodes():
  '''check node'''
  print("Testcase: check_nodes")
  corev1api = getCoreV1Api()
  try:
    ret = corev1api.list_node().to_dict()
  except ApiException as e:
    print("Exception when calling CoreV1Api->list_node: %s\n" % e)
  # check atleast one node is present
  first_node = ret['items'][0]['metadata']['name']
  assert first_node
test_check_nodes()

def test_check_node_health():
  '''check node pressure'''
  node_status = ''
  print("Testcase: check_node_pressures")
  corev1api = getCoreV1Api()
  corev1api = getCoreV1Api()
  try:
    ret = corev1api.list_node().to_dict()
  except ApiException as e:
    print("Exception when calling CoreV1Api->list_node: %s\n" % e)
  # check atleast one node is present
  print(">>status:",ret['items'][0]['status']['conditions'][0])
  for conditions in ret['items'][0]['status']['conditions']:
    print("conditions['type']", conditions['type'])
    if conditions['type'] == 'Ready':
      node_status = conditions['status']
  print("node_status:",node_status)
  # checking the first node to be healthy
  # TODO: check health of all nodes
  assert node_status == 'True'

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
  print("ret:", ret)
  for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

def test_check_deployments():
  '''check deployments'''
  print("Testcase: check_deployments")
  corev1api = getCoreV1Api()

def test_check_services():
  '''check services'''
  print("Testcase: check_services")
  corev1api = getCoreV1Api()
  resp = corev1api.list_service_for_all_namespaces()
  print("resp:", resp)

def test_check_secrets():
  '''check secrets'''
  print("Testcase: check_secrets")
  corev1api = getCoreV1Api()
  resp = corev1api.list_secret_for_all_namespaces()
  print("resp:", resp)

def test_check_service_rechability():
  '''port-forward'''
  print("Testcase: check_service_rechability")
  corev1api = getCoreV1Api()

def test_detect_nonrunning_pods():
  '''pods not running'''
  print("Testcase: detect_nonrunning_pods")
  corev1api = getCoreV1Api()
  ret = corev1api.list_pod_for_all_namespaces(watch=False)
  print("ret:", ret)
  for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

def test_check_configmap_allns():
  print("Testcase: check_configmap_allns")
  corev1api = getCoreV1Api()
  resp = corev1api.list_config_map_for_all_namespaces()
  print("resp:", resp)
