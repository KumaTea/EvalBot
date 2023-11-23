import time
import asyncio
from common.data import *
from eval.docker import *
from pyrogram import Client
from typing import Optional
from pyrogram.types import Message
from pyrogram.enums.parse_mode import ParseMode
from eval.lang.python import create_bash_script
from bot.tools import get_command_content, gen_uuid


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

    inform, _ = asyncio.gather(
        message.reply_text(RUNNING, quote=False),
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

    while time.time() - t0 < limits['timeout']:
        if await container_exited(name):
            output, error, statistic = read_del_output_files(name)
            result_text = gen_result(output, error, statistic)
            inform, _ = await asyncio.gather(
                inform.edit_text(result_text, parse_mode=ParseMode.MARKDOWN),
                clean_container(name)
            )
            return inform
        await asyncio.sleep(1)

    # timeout
    _, _, _ = read_del_output_files(name)
    inform, _ = await asyncio.gather(
        inform.edit_text(TIMEOUT),
        clean_container(name)
    )
    return inform
