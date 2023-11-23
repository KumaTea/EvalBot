import time
import asyncio
import logging
from common.data import *
from pyrogram.types import Message
from pyrogram.enums.parse_mode import ParseMode
from eval.docker import run_docker, container_exited, clean_container, read_output_files, clean_files


def gen_result(output, error, statistic, code_file=None):
    result_text = ''
    if output:
        if len(output.split()) > 3:
            result_text += f'```log\n{output}\n```\n'
        else:
            result_text += f'`{output}`\n'
    else:
        result_text += '(no output)\n'
    if error:
        result_text += '\nError:\n'
        if code_file:
            error.replace(code_file, '<code>')
        if len(error.split()) > 3:
            result_text += f'```log\n{error}\n```\n'
        else:
            result_text += f'`{error}`\n'
    # fix stat later
    return result_text


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
        if container_exited(name):
            logging.info(f'[func.runner run]\t{chat_id=} {name=} exited')
            output, error, statistic = read_output_files(name)
            result_text = gen_result(output, error, statistic, code_file)
            logging.info(f'[func.runner run]\t{chat_id=} {name=} {result_text=}')
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
    result_text = gen_result(output, error, statistic, code_file)
    logging.info(f'[func.runner run]\t{chat_id=} {name=} {result_text=}')
    inform, _ = await asyncio.gather(
        inform.edit_text(f'{TIMEOUT}\n{result_text}', parse_mode=ParseMode.MARKDOWN),
        clean_container(name)
    )
    clean_files(name)
    return inform
