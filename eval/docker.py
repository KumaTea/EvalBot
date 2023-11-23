import asyncio
import logging
from common.data import *


def get_output_files(name: str) -> tuple[str, str, str]:
    return f'{SHM}/{name}-out.txt', f'{SHM}/{name}-err.txt', f'{SHM}/{name}-stat.txt'


def read_output_files(name: str):
    out, err, stat = get_output_files(name)

    if os.path.exists(out):
        with open(out, 'r', encoding='utf-8') as f:
            output = f.read()
    if os.path.exists(err):
        with open(err, 'r', encoding='utf-8') as f:
            error = f.read()
    if os.path.exists(stat):
        with open(stat, 'r', encoding='utf-8') as f:
            statistic = f.read()
    return output, error, statistic


def clean_files(name: str) -> None:
    files = [f for f in os.listdir(SHM) if f.startswith(name)]
    for f in files:
        os.remove(f'{SHM}/{f}')


async def run_docker(
        name: str,
        image: str,
        cmd: str,
        cpu: int = DOCKER_LIMITS['cpu'],
        memory: int = DOCKER_LIMITS['memory'],
        shm_size: int = DOCKER_LIMITS['shm_size'],
        read_only: bool = DOCKER_LIMITS['read_only'],
        no_net: bool = DOCKER_LIMITS['no_net'],
) -> None:
    command = []
    command.extend('docker run'.split())
    # name
    command.extend(['--name', name])
    # detach
    command.append('-d')

    # limits
    # limits: cpu
    command.extend(['--cpus', str(cpu)])
    # limits: memory
    command.extend(['--memory', str(memory)])
    # limits: shm_size
    command.extend(['--shm-size', str(shm_size)])
    # limits: read_only
    if read_only:
        command.append('--read-only')
    # network
    if no_net:
        command.append('--network=none')

    # mounts
    # mounts: shm
    command.extend(['--volume', f'{SHM}:{SHM}'])
    # mounts: GNU time
    command.extend(['--volume', f'/usr/bin/time:/usr/bin/time'])

    # image
    command.append(image)
    # command
    command.extend(cmd.split())

    # not subprocess.run(command)
    # run in background, don't wait
    # subprocess.Popen(command)
    logging.info(f'[eval.docker run_docker]\t{name=} {command=}')
    await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)


async def container_exited(name: str) -> bool:
    command = f'docker inspect --format="{{{{.State.Running}}}}" {name}'
    proc = await asyncio.create_subprocess_exec(*command.split(), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    logging.info(f'[eval.docker container_exited]\t{name=} {stdout=}')
    return stdout.decode().strip() == 'false'


async def clean_container(name: str) -> None:
    stop_command = f'docker stop {name}'
    rm_command = f'docker rm {name}'
    logging.info(f'[eval.docker clean_container]\t{name=} {stop_command=} {rm_command=}')
    await asyncio.create_subprocess_exec(*stop_command.split(), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await asyncio.create_subprocess_exec(*rm_command.split(), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
