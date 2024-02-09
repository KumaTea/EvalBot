import logging
from pyrogram import Client
from bot.tools import gen_uuid
from bot.auth import ensure_auth
from pyrogram.types import Message
from common.data import SHM, DOCKER_IMAGES
from eval.lang.cpp import create_bash_script
from func.lang.common import select_run_lang, command_lang


async def run_cpp(code: str, message: Message, edited: bool = False, inform_id: int = None) -> Message:
    ct_name = 'cp' + gen_uuid()
    filename = f'{SHM}/{ct_name}.cpp'
    real_filename = f'{SHM}/{ct_name}/{ct_name}.cpp'
    logging.info(f'[func.lang.cpp run_cpp]\t{ct_name=} {code=}')
    return await select_run_lang(
        edited=edited,
        code=code,
        message=message,
        ct_name=ct_name,
        image=DOCKER_IMAGES['cpp'],
        filename=filename,
        real_filename=real_filename,
        create_lang_script=create_bash_script,
        inform_id=inform_id,
    )


@ensure_auth
async def command_cpp(client: Client, message: Message) -> Message:
    return await command_lang(client, message, run_cpp)
