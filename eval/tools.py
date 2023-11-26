import logging
import subprocess
from common.data import *


def docker_clean():
    bash = '/bin/bash'
    null = subprocess.DEVNULL
    subprocess.run(REMOVE_UNTAGGED, shell=True, executable=bash, stdout=null, stderr=null)
    subprocess.run(STOP_ALL, shell=True, executable=bash, stdout=null, stderr=null)
    subprocess.run(REMOVE_ALL, shell=True, executable=bash, stdout=null, stderr=null)


def docker_pull():
    for image in DOCKER_IMAGES.values():
        r = subprocess.run(f'docker pull {image}', shell=True)
        result = r.stdout.decode('utf-8')
        if 'newer image' in result:
            logging.info('[eval.tools docker_pull]\t' + result.splitlines()[-1])
