from common.info import *


if debug_mode:
    pwd = r'D:\GitHub\EvalBot'
else:
    pwd = '/root/EvalBot'

SHM = '/dev/shm'


DOCKER_IMAGES = {
    # If there is a stable version, use it.
    # Otherwise, use the slim image
    # based on Debian's latest stable version.

    'bash':    'debian:12-slim',
    'c':       'buildpack-deps:bookworm',
    'cpp':     'buildpack-deps:bookworm',
    'build':   'buildpack-deps:bookworm',
    'node':    'node:lts-slim',
    'perl':    'perl:slim',
    'ruby':    'ruby:slim',
    'python':  'python:3.12-slim',
    'busybox': 'busybox:stable',
}

LANG_CMDS = {
    'bash':    ['bash', 'sh', 'shell'],
    'c':       ['c', 'gcc', 'clang'],
    'cpp':     ['cpp'],  # 'c++' and 'g++' cause regex errors
    'build':   ['build'],
    'node':    ['node', 'js', 'nodejs', 'javascript'],
    'perl':    ['perl', 'pl'],
    'ruby':    ['ruby', 'rb'],
    'python':  ['python', 'py', 'python3'],
    'busybox': ['busybox', 'ash'],
}

MiB = 1024 * 1024

DOCKER_LIMITS = {
    'cpu': 1,
    'memory': 64 * MiB,
    'timeout': 60,
    'shm_size': 64 * MiB,
    'read_only': False,
    'disk_quota': 64 * MiB,
    'no_net': True,
}

TRUSTED_LIMITS = {
    'cpu': 4,
    'memory': 256 * MiB,
    'timeout': 120,
    'shm_size': 256 * MiB,
    'read_only': False,
    'disk_quota': 256 * MiB,
    'no_net': False,
}

# COMMON_LIMITS = {
#     'write_bps': '10m',
# }

NO_CODE = '未提供代码。'
CREATING = '正在创建 `{IMAGE}` 容器...'
RUNNING = '正在创建 `{IMAGE}` 容器...完成\n正在运行...'
TIMEOUT = '任务超时！'

# commands
REMOVE_UNTAGGED = 'docker rmi $(docker images -f "dangling=true" -q)'
STOP_ALL = 'docker stop $(docker ps -a -q)'
REMOVE_ALL = 'docker rm $(docker ps -a -q)'
