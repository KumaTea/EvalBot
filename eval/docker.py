import shutil
import asyncio
import logging
from common.data import *


def get_output_files(name: str, real_path: bool) -> tuple[str, str, str, str]:
    if real_path:
        path = f'{SHM}/{name}'
    else:
        path = SHM
    return (
        f'{path}/out.txt',
        f'{path}/err.txt',
        f'{path}/stat.txt',
        f'{path}/exit.txt'
    )


def trim_text(text: str) -> str:
    while text.startswith('\n'):
        text = text[1:]
    while text.endswith('\n'):
        text = text[:-1]
    return text


def read_output_files(name: str):
    out, err, stat, _ = get_output_files(name, real_path=True)
    output, error, statistic = '', '', ''
    try:
        if os.path.exists(out):
            with open(out, 'r', encoding='utf-8') as f:
                output = f.read()
            output = trim_text(output)
        if os.path.exists(err):
            with open(err, 'r', encoding='utf-8') as f:
                error = f.read()
            error = trim_text(error)
    except UnicodeDecodeError:
        error = 'UnicodeDecodeError'
    if os.path.exists(stat):
        with open(stat, 'r', encoding='utf-8') as f:
            statistic = f.read()
        statistic = trim_text(statistic)
    # logging.info(f'[eval.docker read_output_files]\t{name=} {output=} {error=} {statistic=}')
    return output, error, statistic


def clean_files(name: str) -> None:
    # files = [f for f in os.listdir(SHM) if f.startswith(name)]
    # for f in files:
    #     os.remove(f'{SHM}/{f}')
    return shutil.rmtree(f'{SHM}/{name}')


async def run_docker(
        name: str,
        image: str,
        cmd: str,
        cpu: int = DOCKER_LIMITS['cpu'],
        memory: int = DOCKER_LIMITS['memory'],
        shm_size: int = DOCKER_LIMITS['shm_size'],
        read_only: bool = DOCKER_LIMITS['read_only'],
        disk_quota: int = None,
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
    # limits: disk_quota
    if disk_quota:
        command.extend(['--storage-opt', f'size={disk_quota}'])
    # network
    if no_net:
        command.append('--network=none')

    # mounts
    # mounts: shm
    command.extend(['--volume', f'{SHM}/{name}:{SHM}'])
    # mounts: GNU time
    command.extend(['--volume', f'/usr/bin/time:/usr/bin/time:ro'])

    # image
    command.append(image)
    # command
    command.extend(cmd.split())

    # not subprocess.run(command)
    # run in background, don't wait
    # subprocess.Popen(command)
    logging.info(f'[eval.docker run_docker]\t{name=} command={" ".join(command)}')
    await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)


def container_exited(name: str) -> bool:
    _, _, _, exit_sign = get_output_files(name, real_path=True)
    return os.path.exists(exit_sign)


async def clean_container(name: str) -> None:
    stop_command = f'docker stop {name}'
    rm_command = f'docker rm {name}'
    combined = f'{stop_command} && {rm_command}'
    logging.info(f'[eval.docker clean_container]\t{name=} {stop_command=} {rm_command=}')
    # p = await asyncio.create_subprocess_exec(*stop_command.split(), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    # # ensure done
    # await p.communicate()
    # await asyncio.create_subprocess_exec(*rm_command.split(), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await asyncio.create_subprocess_shell(combined, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
