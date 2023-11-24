import logging
from pyrogram import Client
from bot.tools import gen_uuid
from pyrogram.types import Message
from common.data import SHM, DOCKER_IMAGES
from eval.lang.node import create_bash_script
from func.lang.common import run_lang, command_lang


async def run_node(code: str, message: Message) -> Message:
    ct_name = 'js' + gen_uuid()
    filename = f'{SHM}/{ct_name}.js'
    real_filename = f'{SHM}/{ct_name}/{ct_name}.js'
    logging.info(f'[func.lang.node run_node]\t{ct_name=} {code=}')
    return await run_lang(
        code=code,
        message=message,
        ct_name=ct_name,
        image=DOCKER_IMAGES['node'],
        filename=filename,
        real_filename=real_filename,
        create_lang_script=create_bash_script,
        executor='bash',
    )


async def command_node(client: Client, message: Message) -> Message:
    return await command_lang(client, message, run_node)
