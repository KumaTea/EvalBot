import logging
import subprocess
from common.data import *


def analyze_stat(stat: str):
    used_time = '?:??.??'
    peak_mem = '?'
    exit_code = '?'
    for line in stat.split('\n'):
        if 'Elapsed (wall clock) time (h:mm:ss or m:ss)' in line:
            used_time = line.split(': ')[1]
        elif 'Maximum resident set size (kbytes): ' in line:
            peak_mem = line.split(': ')[1]
        elif 'Exit status: ' in line:
            exit_code = line.split(': ')[1]
    return used_time, peak_mem, exit_code


def format_ram_usage(peak_mem: str) -> str:
    mem_usage = int(peak_mem)
    if mem_usage < 1024:
        return f'{mem_usage} KB'
    elif mem_usage < 1024 * 1024:
        return f'{mem_usage / 1024:.3f} MB'
    else:
        return f'{mem_usage / 1024 / 1024:.3f} GB'


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
