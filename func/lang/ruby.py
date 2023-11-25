import logging
from pyrogram import Client
from bot.tools import gen_uuid
from pyrogram.types import Message
from bot.auth import ensure_not_bl
from common.data import SHM, DOCKER_IMAGES
from eval.lang.ruby import create_bash_script
from func.lang.common import run_lang, command_lang


async def run_ruby(code: str, message: Message) -> Message:
    ct_name = 'rb' + gen_uuid()
    filename = f'{SHM}/{ct_name}.rb'
    real_filename = f'{SHM}/{ct_name}/{ct_name}.rb'
    logging.info(f'[func.lang.ruby run_ruby]\t{ct_name=} {code=}')
    return await run_lang(
        code=code,
        message=message,
        ct_name=ct_name,
        image=DOCKER_IMAGES['ruby'],
        filename=filename,
        real_filename=real_filename,
        create_lang_script=create_bash_script,
    )


@ensure_not_bl
async def command_ruby(client: Client, message: Message) -> Message:
    return await command_lang(client, message, run_ruby)
