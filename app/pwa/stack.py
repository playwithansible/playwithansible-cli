
from jinja2 import Template
from typing import List

import errno
import os
import re
import subprocess

__version__ = "0.2.2"

dir_run = "/var/run/playwithansible"
file_template_compose = "templates/docker-compose.yml.j2"
file_template_compose_testing = "templates/docker-compose-testing.yml.j2"
file_template_inventory = "templates/inventory.ini.j2"

docker_registry = "ghcr.io"
docker_namespace = "playwithansible"

def template_to_file(src_file: str, dst_file: str, **kwargs):
    template = Template(open(src_file).read())
    content = template.render(
        kwargs
        )
    with open(dst_file, "w+") as output_file:
        print(content, file=output_file)

def create_directory(dir: str):
    try:
        os.makedirs(dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print(f"Creation of the directory '{dir}' failed ({e})")

def create_stack(stackname: str, distributions: List[str]):
    dir_stack = f"{dir_run}/{stackname}"
    dir_stack_inventories = f"{dir_stack}/ansible/inventories"
    create_directory(dir_stack_inventories)
    create_directory(f"{dir_stack_inventories}/groupvars")
    create_directory(f"{dir_stack_inventories}/hostvars")

    pwa_distributions = dict()
    for d in distributions:
        m = re.match(r'^(\w+?)(\d+)$', d)
        name, version = m[1], m[2]
        if name in pwa_distributions:
            pwa_distributions[name]['versions'].append(version)
        else:
            pwa_distributions[name] = { 'versions': [ version ] }
    
    template_to_file(
        file_template_compose,
        f"{dir_stack}/docker-compose.yml",
        registry=docker_registry,
        registry_namespace=docker_namespace,
        pwa_stackname=stackname,
        pwa_version=__version__, 
        pwa_distributions=distributions 
        )
    template_to_file(
        file_template_inventory,
        f"{dir_stack_inventories}/inventory.ini",
        pwa_version=__version__, 
        pwa_distributions=pwa_distributions 
        )

def create_stack_testing(stackname: str, ansible_versions: List[str], distributions: List[str]):
    dir_stack = f"{dir_run}/{stackname}"
    dir_stack_inventories = f"{dir_stack}/ansible/inventories"
    create_directory(dir_stack_inventories)
    create_directory(f"{dir_stack_inventories}/groupvars")
    create_directory(f"{dir_stack_inventories}/hostvars")

    pwa_distributions = dict()
    for d in distributions:
        m = re.match(r'^(\w+?)(\d+)$', d)
        name, version = m[1], m[2]
        if name in pwa_distributions:
            pwa_distributions[name]['versions'].append(version)
        else:
            pwa_distributions[name] = { 'versions': [ version ] }
    
    template_to_file(
        file_template_compose_testing,
        f"{dir_stack}/docker-compose.yml",
        registry=docker_registry,
        registry_namespace=docker_namespace,
        pwa_stackname=stackname,
        pwa_version=__version__,
        ansible_versions=ansible_versions, 
        pwa_distributions=distributions 
        )
    template_to_file(
        file_template_inventory,
        f"{dir_stack_inventories}/inventory.ini",
        pwa_version=__version__, 
        pwa_distributions=pwa_distributions 
        )

def start_stack(stackname: str):
    dir = f"{dir_run}/{stackname}"
    process = subprocess.run(
        ['docker-compose', 
        '-f', f"{dir}/docker-compose.yml", 
        '-p', f"pwa_{stackname}",
        'up'],
        stdout=subprocess.PIPE, 
        universal_newlines=True)
    print(process.stdout)

def stop_stack(stackname: str):
    dir = f"{dir_run}/{stackname}"
    process = subprocess.run(
        ['docker-compose', 
        '-f', f"{dir}/docker-compose.yml", 
        '-p', f"pwa_{stackname}",
        'down'],
        stdout=subprocess.PIPE, 
        universal_newlines=True)
    print(process.stdout)