import logging
from common.data import *
from pyrogram import Client
from bot.tools import gen_uuid
from pyrogram.types import Message
from bot.auth import ensure_not_bl
from eval.lang.busybox import create_bash_script
from func.lang.common import run_lang, command_lang


async def run_busybox(code: str, message: Message) -> Message:
    ct_name = 'bb' + gen_uuid()
    filename = f'{SHM}/{ct_name}.sh'
    real_filename = f'{SHM}/{ct_name}/{ct_name}.sh'
    logging.info(f'[func.lang.busybox run_busybox]\t{ct_name=} {code=}')
    return await run_lang(
        code=code,
        message=message,
        ct_name=ct_name,
        image=DOCKER_IMAGES['busybox'],
        filename=filename,
        real_filename=real_filename,
        create_lang_script=create_bash_script,
        script_executor='sh',
    )


@ensure_not_bl
async def command_busybox(client: Client, message: Message) -> Message:
    return await command_lang(client, message, run_busybox)
