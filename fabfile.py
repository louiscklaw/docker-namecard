#!/usr/bin/env python
# init_py_dont_write_bytecode

#init_boilerplate

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.project import *

CWD = os.path.dirname(__file__)
# PROJ_HOME = [CWD, '/home/pi/docker-files']
PROJ_HOME=[CWD, '/srv/docker-files/docker-namecard']
NODEJS_PROJ_PATH = PROJ_HOME[1]+'/nodejs'

def sync_to_pi():
    rsync_project(
        local_dir=PROJ_HOME[0]+'/',
        remote_dir=PROJ_HOME[1],
        delete=True
    )


def build_docker_image():
    print('build docker image')

    with cd(NODEJS_PROJ_PATH):
        run('docker build -f Dockerfile -t nodejs_tryout .')


def build_docker_compose():
    with cd(NODEJS_PROJ_PATH):
        run('docker-compose build')
        run('docker-compose kill && docker-compose down')
        run('docker-compose up -d')
        run('docker-compose ps')

def docker_compose_down_and_up(target_container):
    run('docker-compose kill {container} && docker-compose up {container}'.format(
        container=target_container
    ))

@task
@hosts(['logic@gcp.louislabs.com'])
def rebuild():
    sudo('chown -R logic:logic {}'.format(PROJ_HOME[1]))
    local('rsync -azhW --delete {}/ logic@gcp.louislabs.com:{}'.format(
        PROJ_HOME[0], PROJ_HOME[1]
    ))

    with settings(warn_only=True):
        run('docker network create web')

    with cd(PROJ_HOME[1]):
        run('docker image prune --force --all')
        run('docker-compose build --no-cache contacts_nodejs')
        run('docker-compose up -d contacts_nodejs')
        run('docker image prune --force --all')
