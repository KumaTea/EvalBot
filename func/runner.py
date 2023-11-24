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


def wrap_code(text: str, long=True):
    if long:
        if '```' in text:
            result = f'<pre lang="log">\n{text}\n</pre>'
        else:
            result = f'```\n{text}\n```'
    else:
        if '`' in text:
            result = f'<code>{text}</code>'
        else:
            result = f'`{text}`'
    return result


def gen_result(output, error, statistic, code_file=None):
    result_text = ''
    if output:
        text = gen_output(output)
        is_long = len(output.splitlines()) > 3
        result_text += wrap_code(text, long=is_long)
    if error:
        result_text += '\nERROR:\n'
        if code_file:
            error = error.replace(code_file, '[code]')
        text = gen_output(error)
        is_long = len(error.splitlines()) > 3
        result_text += wrap_code(text, long=is_long)
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
        inform.edit_text(text),
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
                await inform.edit_text(RUNNING)

    # timeout
    inform = await read_and_finish(name, code_file, inform, timeout=True)
    return inform
