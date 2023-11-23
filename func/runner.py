import time
import asyncio
import logging
from common.data import *
from eval.docker import run_docker, container_exited, clean_container, read_output_files, clean_files
from pyrogram.types import Message
from pyrogram.enums.parse_mode import ParseMode


def gen_result(output, error, statistic):
    result_text = ''
    if output:
        if len(output.split('\n')) > 3:
            result_text += f'```log\n{output}\n```\n'
        else:
            result_text += f'`{output}`\n'
    if error:
        result_text += '\nError:\n'
        if len(error.split('\n')) > 3:
            result_text += f'```log\n{error}\n```\n'
        else:
            result_text += f'`{error}`\n'
    # fix stat later
    return result_text


async def run(message: Message, command: str, name: str, image: str) -> Message:
    chat_id = message.chat.id
    if chat_id in trusted_group:
        limits = TRUSTED_LIMITS
    else:
        limits = DOCKER_LIMITS
    logging.info(f'[func.runner run]\t{chat_id=} {name=} {image=} {command=}')

    inform, _ = await asyncio.gather(
        message.reply_text(CREATING, quote=False),
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
        if await container_exited(name):
            logging.info(f'[func.runner run]\t{chat_id=} {name=} exited')
            output, error, statistic = read_output_files(name)
            result_text = gen_result(output, error, statistic)
            inform, _ = await asyncio.gather(
                inform.edit_text(result_text, parse_mode=ParseMode.MARKDOWN),
                clean_container(name)
            )
            clean_files(name)
            return inform
        else:
            if not creation_informed and time.time() - t0 > 5:
                creation_informed = True
                logging.info(f'[func.runner run]\t{chat_id=} {name=} creation_informed')
                await inform.edit_text(RUNNING, parse_mode=ParseMode.MARKDOWN)

        await asyncio.sleep(1)

    # timeout
    logging.info(f'[func.runner run]\t{chat_id=} {name=} timeout')
    output, error, statistic = read_output_files(name)
    result_text = gen_result(output, error, statistic)

    inform, _ = await asyncio.gather(
        inform.edit_text(f'{TIMEOUT}\n{result_text}', parse_mode=ParseMode.MARKDOWN),
        clean_container(name)
    )
    clean_files(name)
    return inform
