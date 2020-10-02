# Playwithansible Command Line Interface

## Build

```shell
docker build -t ghcr.io/playwithansible/playwithansible-cli:0.2.2 .
```

## Run

### User mode

```shell
docker run -it \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /var/run/playwithansible:/var/run/playwithansible \
    ghcr.io/playwithansible/playwithansible-cli:0.2.2 bash

# create a stack name 'latest' with Ansible 2.9.10
playwithansible create -d debian9 -d centos8 -d ubuntu2004 -d fedora32 -a 2.9.10 latest

# create a testing stack named 'testing' with Ansible 2.8.12,2.9.10
playwithansible create-testing -d debian10 -d fedora32 -a 2.8.12 -a 2.9.10 testing
```

### Devel mode

```shell
docker run -it \
    -v $PWD:/local \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /var/run/playwithansible:/var/run/playwithansible \
    -w /local/app \
    ghcr.io/playwithansible/playwithansible-cli:0.2.2 bash
```
