import logging
from pyrogram import Client
from bot.tools import gen_uuid
from share.auth import ensure_auth
from pyrogram.types import Message
from common.data import SHM, DOCKER_IMAGES
from eval.lang.ruby import create_bash_script
from func.lang.common import command_lang, select_run_lang


async def run_ruby(code: str, message: Message, edited: bool = False, inform_id: int = None) -> Message:
    ct_name = 'rb' + gen_uuid()
    filename = f'{SHM}/{ct_name}.rb'
    real_filename = f'{SHM}/{ct_name}/{ct_name}.rb'
    logging.info(f'[func.lang.ruby run_ruby]\t{ct_name=} {code=}')
    return await select_run_lang(
        edited=edited,
        code=code,
        message=message,
        ct_name=ct_name,
        image=DOCKER_IMAGES['ruby'],
        filename=filename,
        real_filename=real_filename,
        create_lang_script=create_bash_script,
        inform_id=inform_id
    )


@ensure_auth
async def command_ruby(client: Client, message: Message) -> Message:
    return await command_lang(client, message, run_ruby)
