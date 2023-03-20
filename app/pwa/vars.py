import os
import yaml

__version__ = "0.3.0"

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/data'
pwa_run_dir = "/var/run/playwithansible"

with open(f'{data_dir}/ansible_versions.yml') as file:
    config = yaml.full_load(file)
supported_ansible_versions = config['ansible_versions']

with open(f'{data_dir}/distribution_versions.yml') as file:
    config = yaml.full_load(file)
supported_distributions = []
for d in config['distribution_versions']:
    supported_distributions.append(d['name'])
