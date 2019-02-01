#!/usr/bin/env python3

try:
  import kubernetes
except ImportError:
  print("kubernetes package not installed, run \"pip3 install kubernetes\"")

try:
  import click
except ImportError:
  print("click package not installed, run \"pip3 install click\"")

@click.command()
@click.option('--name', '-n',help='k8s deployment name')
@click.option('--image','-i',help='docker image to use')

def deployment(name,image):
  click.echo('Deploying ....')

if __name__ == '__main__':
  deployment()
