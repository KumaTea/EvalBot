from common.info import *


try:
    from local_db import trusted_group, bl_users
except ImportError:
    trusted_group = []
    bl_users = []

if debug_mode:
    PWD = r'D:\GitHub\EvalBot'
else:
    PWD = '/root/EvalBot'

SHM = '/dev/shm'


DOCKER_IMAGES = {
    'python': 'python:3.12-slim',
    'python2': 'python:2.7',
    # 'bash': 'bash:latest',
    'bash': 'debian:12-slim'
}

MiB = 1024 * 1024

DOCKER_LIMITS = {
    'cpu': 1,
    'memory': 64 * MiB,
    'timeout': 60,
    'shm_size': 64 * MiB,
    'read_only': True,
    'no_net': True,
}

TRUSTED_LIMITS = {
    'cpu': 4,
    'memory': 256 * MiB,
    'timeout': 120,
    'shm_size': 256 * MiB,
    'read_only': False,
    'no_net': False,
}

NO_CODE = '未提供代码。'
CREATING = '正在创建任务...'
RUNNING = '正在创建任务...已完成\n正在运行...'
TIMEOUT = '任务超时。'
