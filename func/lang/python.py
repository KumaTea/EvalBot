import logging
from pyrogram import Client
from bot.tools import gen_uuid
from pyrogram.types import Message
from common.data import SHM, DOCKER_IMAGES
from eval.lang.python import create_bash_script
from func.lang.common import run_lang, command_lang


async def run_python(code: str, message: Message) -> Message:
    ct_name = 'py' + gen_uuid()
    filename = f'{SHM}/{ct_name}.py'
    real_filename = f'{SHM}/{ct_name}/{ct_name}.py'
    logging.info(f'[func.lang.python run_python]\t{ct_name=} {code=}')
    return await run_lang(
        code=code,
        message=message,
        ct_name=ct_name,
        image=DOCKER_IMAGES['python'],
        filename=filename,
        real_filename=real_filename,
        create_lang_script=create_bash_script,
        executor='bash',
    )


async def command_python(client: Client, message: Message) -> Message:
    return await command_lang(client, message, run_python)
