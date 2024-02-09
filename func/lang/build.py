import logging
from pyrogram import Client
from bot.tools import gen_uuid
from bot.auth import ensure_auth
from pyrogram.types import Message
from common.data import SHM, DOCKER_IMAGES
from eval.lang.build import create_bash_script
from func.lang.common import select_run_lang, command_lang


async def run_build(code: str, message: Message, edited: bool = False, inform_id: int = None) -> Message:
    ct_name = 'bu' + gen_uuid()
    filename = f'{SHM}/{ct_name}.sh'
    real_filename = f'{SHM}/{ct_name}/{ct_name}.sh'
    logging.info(f'[func.lang.build run_build]\t{ct_name=} {code=}')
    return await select_run_lang(
        edited=edited,
        code=code,
        message=message,
        ct_name=ct_name,
        image=DOCKER_IMAGES['build'],
        filename=filename,
        real_filename=real_filename,
        create_lang_script=create_bash_script,
        inform_id=inform_id
    )


@ensure_auth
async def command_build(client: Client, message: Message) -> Message:
    return await command_lang(client, message, run_build)
