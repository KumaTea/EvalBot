import time
import asyncio
import logging
from common.data import *
from func.tools import gen_result
from pyrogram.types import Message
from eval.docker import run_docker, container_exited, clean_container, read_output_files, clean_files


async def read_and_finish(name: str, code_file: str = None, inform: Message = None, timeout=False) -> Message:
    output, error, statistic = read_output_files(name)
    result_text, parse_mode = gen_result(output, error, statistic, code_file)
    # logging.info(f'[func.runner run]\t{chat_id=} {name=} {result_text=}')
    if timeout:
        text = f'{TIMEOUT}\n{result_text}'
    else:
        text = result_text
    inform, _ = await asyncio.gather(
        inform.edit_text(text, parse_mode=parse_mode),
        clean_container(name)
    )
    clean_files(name)
    return inform


async def run(
        message: Message,
        command: str,
        name: str,
        image: str,
        code_file: str = None,
) -> Message:
    chat_id = message.chat.id
    trusted = chat_id in trusted_group
    limits = TRUSTED_LIMITS if trusted else DOCKER_LIMITS
    logging.info(f'[func.runner run]\t{chat_id=} {trusted=} {name=} {image=} {command=}')

    inform, _ = await asyncio.gather(
        message.reply_text(CREATING.format(IMAGE=image), quote=False),
        run_docker(
            name=name,
            image=image,
            cmd=command,
            cpu=limits['cpu'],
            memory=limits['memory'],
            shm_size=limits['shm_size'],
            read_only=limits['read_only'],
            no_net=limits['no_net'],
        )
    )
    t0 = time.time()
    creation_informed = False

    while time.time() - t0 < limits['timeout']:
        await asyncio.sleep(1)

        if container_exited(name):
            logging.info(f'[func.runner run]\t{chat_id=} {name=} exited')
            inform = await read_and_finish(name, code_file, inform)
            return inform
        else:
            if not creation_informed and time.time() - t0 > 5:
                creation_informed = True
                logging.info(f'[func.runner run]\t{chat_id=} {name=} creation_informed')
                await inform.edit_text(RUNNING.format(IMAGE=image))

    # timeout
    inform = await read_and_finish(name, code_file, inform, timeout=True)
    return inform
