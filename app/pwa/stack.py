from jinja2 import Template
from rich.console import Console
from rich.table import Table
from typing import List

import errno
import json
import os
import pathlib
import re
import subprocess

from pwa.docker_compose import compose_down, compose_up
from pwa.utils import print_colored_distributions, stack_nb_items, stacks_list
from pwa.vars import __version__,pwa_run_dir

dir_templates = pathlib.Path(__file__).parent / "../templates"
file_template_compose = f"{dir_templates}/docker-compose.yml.j2"
file_template_deployment = f"{dir_templates}/pwa-deployment.yml.j2"
file_template_inventory = f"{dir_templates}/inventory.ini.j2"

docker_registry = "ghcr.io"
docker_namespace = "playwithansible"

def template_to_file(src_file: str, dst_file: str, **kwargs):
    template = Template(open(src_file).read())
    content = template.render(
        kwargs
        )
    with open(dst_file, "w+") as output_file:
        print(content, file=output_file)

def create_directory(directory: str):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print(f"Creation of the directory '{directory}' failed ({e})")

def create_stack(stackname: str, ansible_versions: List[str], distributions: List[str]):
    dir_stack = f"{pwa_run_dir}/{stackname}"
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
    pwa_ansible_versions = []
    for v in ansible_versions:
        pwa_ansible_versions.append(v)
    stack_data = {
        'ansible': pwa_ansible_versions,
        'distributions': pwa_distributions
    }
    with open(f"{dir_stack}/stack.json", 'w') as outfile:
        json.dump(stack_data, outfile)

    template_to_file(
        file_template_compose,
        f"{dir_stack}/docker-compose.yml",
        registry=docker_registry,
        registry_namespace=docker_namespace,
        pwa_stackname=stackname,
        pwa_version=__version__,
        pwa_ansible_versions=pwa_ansible_versions,
        pwa_distributions=distributions
        )
    template_to_file(
        file_template_deployment,
        f"{dir_stack}/pwa-deployment.yml",
        registry=docker_registry,
        registry_namespace=docker_namespace,
        pwa_stackname=stackname,
        pwa_version=__version__,
        pwa_ansible_versions=pwa_ansible_versions,
        pwa_distributions=distributions
        )
    template_to_file(
        file_template_inventory,
        f"{dir_stack_inventories}/inventory.ini",
        pwa_version=__version__,
        pwa_distributions=pwa_distributions
        )


def stack_info(stackname: str):
    print_colored_distributions(stackname)

def stack_status(stackname: str):
    dir = f"{pwa_run_dir}/{stackname}"
    nb_items = stack_nb_items(stackname)
    process = subprocess.run(
        ['docker-compose',
        '-f', f"{dir}/docker-compose.yml",
        '-p', f"pwa_{stackname}",
        'ps' , '-q', '--filter', 'State=Up'],
        stdout=subprocess.PIPE,
        universal_newlines=True)
    nb_lines = len(process.stdout.splitlines())
    status = 'Stopped'
    if nb_lines == nb_items:
        status = 'Started'
    elif nb_lines > 0 and nb_lines != nb_items:
        status = 'Errors'
    
    return (status)

def stack_list():
    console = Console()
    table = Table()
    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Distributions", style="magenta")
    table.add_column("Status", justify="center", style="green")
    stacks = stacks_list()
    for stack in stacks:
        status = stack_status(stack)
        table.add_row(stack, print_colored_distributions(stack), status)
    console.print(table)


def start_stack(stackname: str):
    compose_up(stackname)

def stop_stack(stackname: str):
    compose_down(stackname)

def test_on_stack(stackname: str, rolename: str):
    pass