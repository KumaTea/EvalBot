import time
import asyncio
import logging
from common.data import *
from pyrogram.types import Message
from pyrogram.enums.parse_mode import ParseMode
from eval.docker import run_docker, container_exited, clean_container, read_output_files, clean_files


def gen_output(output: str, limit: int = 2000):
    if len(output) > limit:
        notify = f'(too long! Last {limit} chars are shown)'
        count = len(notify) + 1
        out = []
        for line in reversed(output.splitlines()):
            if count + len(line) + 1 < limit:
                out.insert(0, line)
                count += len(line) + 1
            else:
                break
        out.insert(0, notify)
        output = '\n'.join(out)
    return output


def gen_result(output, error, statistic, code_file=None):
    result_text = ''
    if output:
        text = gen_output(output)
        if len(output.splitlines()) > 3:
            result_text += f'```log\n{text}\n```\n'
        else:
            result_text += f'`{text}`\n'
    if error:
        result_text += '\nERROR:\n'
        if code_file:
            error = error.replace(code_file, '<code>')
        text = gen_output(error)
        if len(error.splitlines()) > 3:
            result_text += f'```log\n{text}\n```\n'
        else:
            result_text += f'`{text}`\n'
    if not result_text:
        result_text = '(no output)'
    # fix stat later
    return result_text


async def read_and_finish(name: str, code_file: str = None, inform: Message = None, timeout=False) -> Message:
    output, error, statistic = read_output_files(name)
    result_text = gen_result(output, error, statistic, code_file)
    # logging.info(f'[func.runner run]\t{chat_id=} {name=} {result_text=}')
    if timeout:
        text = f'{TIMEOUT}\n{result_text}'
    else:
        text = result_text
    inform, _ = await asyncio.gather(
        inform.edit_text(text, parse_mode=ParseMode.MARKDOWN),
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
        await asyncio.sleep(1)

        if container_exited(name):
            logging.info(f'[func.runner run]\t{chat_id=} {name=} exited')
            inform = await read_and_finish(name, code_file, inform)
            return inform
        else:
            if not creation_informed and time.time() - t0 > 5:
                creation_informed = True
                logging.info(f'[func.runner run]\t{chat_id=} {name=} creation_informed')
                await inform.edit_text(RUNNING, parse_mode=ParseMode.MARKDOWN)

    # timeout
    inform = await read_and_finish(name, code_file, inform, timeout=True)
    return inform
