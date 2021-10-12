import yaml

__version__ = "0.2.4"

pwa_run_dir = "/var/run/playwithansible"

with open(r'data/ansible_versions.yml') as file:
    config = yaml.full_load(file)
supported_ansible_versions = config['ansible_versions']

with open(r'data/distribution_versions.yml') as file:
    config = yaml.full_load(file)
supported_distributions = []
for d in config['distribution_versions']:
    supported_distributions.append(d['name'])
