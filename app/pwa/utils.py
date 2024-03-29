from pathlib import Path
from rich.style import Style
from rich.text import Text

import json

from pwa.vars import pwa_run_dir


distrib_style = {
    # https://encycolorpedia.com/search?q=https%3a%2f%2fupload.wikimedia.org%2fwikipedia%2fcommons%2fthumb%2fb%2fbf%2fCentos-logo-light.svg%2flangfr-280px-Centos-logo-light.svg.png
    'centos': Style(bgcolor='#9dce25', color='black'),
    # https://encycolorpedia.com/search?q=https%3a%2f%2fupload.wikimedia.org%2fwikipedia%2fcommons%2fthumb%2f4%2f4a%2fDebian-OpenLogo.svg%2flangfr-96px-Debian-OpenLogo.svg.png
    'debian': Style(bgcolor='#d6054a', color='black'),
    # https://encycolorpedia.com/search?q=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F3%2F3f%2FFedora_logo.svg
    'fedora': Style(bgcolor='#294172', color='black'),
    # https://encycolorpedia.com/search?q=https%3a%2f%2fupload.wikimedia.org%2fwikipedia%2fcommons%2fthumb%2fa%2fab%2fLogo-ubuntu_cof-orange-hex.svg%2f100px-Logo-ubuntu_cof-orange-hex.svg.png
    'ubuntu': Style(bgcolor='#dd4814', color='black')
    }


def print_colored_distributions(stackname: str):
    """
    Prints distributions with colors
    """
    config = stack_config(stackname)
    text = Text()
    for distrib in config['distributions']:
        versions = "/".join(config['distributions'][distrib]['versions'])
        distrib_versions = f"{distrib[0:3].capitalize()} {versions}"
        text.append(distrib_versions, style=distrib_style[distrib])
        text.append(" ")

    return text


def stack_config(stackname: str):
    """
    Returns stack <stackanme> configuration
    """
    dir_stack = f"{pwa_run_dir}/{stackname}"
    with open(f"{dir_stack}/stack.json") as json_file:
        data = json.load(json_file)
    
    return data


def stack_nb_items(stackname: str):
    """
    Returns number of items in stack <stackname>
    """
    config = stack_config(stackname)
    count = 0
    count += len(config['ansible'])
    for distrib in config['distributions']:
        for version in config['distributions'][distrib]['versions']:
            count += 1
    
    return count


def stacks_list():
    """
    Returns stacks list
    """    
    p = Path(pwa_run_dir)
    if p.exists() and p.is_dir():
        stacks = [f.name for f in p.iterdir() if f.is_dir()]
        return stacks
    return []
