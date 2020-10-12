import subprocess

from pwa.vars import pwa_run_dir

def compose_down(stackname: str):
    compose_file = f"{pwa_run_dir}/{stackname}/docker-compose.yml"
    project_name = f"pwa_{stackname}"
    process = subprocess.run(
        ['docker-compose', 
        '-f', compose_file, 
        '-p', project_name,
        'down'],
        stdout=subprocess.PIPE, 
        universal_newlines=True)
    #print(process.stdout)

def compose_up(stackname: str):
    compose_file = f"{pwa_run_dir}/{stackname}/docker-compose.yml"
    project_name = f"pwa_{stackname}"
    process = subprocess.run(
        ['docker-compose',
        '-f', compose_file, 
        '-p', project_name,
        'up', '-d' ],
        stdout=subprocess.PIPE, 
        universal_newlines=True)
    #print(process.stdout)