import logging
import subprocess
from common.data import *


def analyze_stat(stat: str):
    used_time = ''
    peak_mem = ''
    for line in stat.split('\n'):
        if 'Elapsed (wall clock) time (h:mm:ss or m:ss)' in line:
            used_time = line.split(': ')[1]
        elif 'Maximum resident set size (kbytes): ' in line:
            peak_mem = line.split(': ')[1]
    return used_time, peak_mem


def format_ram_usage(peak_mem: str) -> str:
    mem_usage = int(peak_mem)
    if mem_usage < 1024:
        return f'{mem_usage} KB'
    elif mem_usage < 1024 * 1024:
        return f'{mem_usage / 1024:.3f} MB'
    else:
        return f'{mem_usage / 1024 / 1024:.3f} GB'


def startup_clean():
    subprocess.run(REMOVE_UNTAGGED, shell=True)
    subprocess.run(STOP_ALL, shell=True)
    subprocess.run(REMOVE_ALL, shell=True)


def pull_all():
    for image in DOCKER_IMAGES.values():
        subprocess.run(f'docker pull {image}', shell=True)
