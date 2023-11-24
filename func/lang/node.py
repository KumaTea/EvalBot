import logging
from common.data import *
from pyrogram import Client
from typing import Optional
from func.runner import run
from pyrogram.types import Message
from bot.auth import ensure_not_bl
from eval.lang.node import create_bash_script
from bot.tools import get_command_content, gen_uuid


async def run_node(code: str, message: Message) -> Message:
    ct_name = 'js' + gen_uuid()  # container_name
    os.mkdir(f'{SHM}/{ct_name}')
    filename = f'{SHM}/{ct_name}.js'
    real_filename = f'{SHM}/{ct_name}/{ct_name}.js'
    logging.info(f'[func.lang.node run_node]\t{ct_name=} {code=}')
    with open(real_filename, 'w', encoding='utf-8') as f:
        f.write(code)
    bash_file = create_bash_script(ct_name, filename)
    command = f'bash {bash_file}'
    return await run(
        message=message,
        command=command,
        name=ct_name,
        image=DOCKER_IMAGES['node'],
        code_file=filename,
    )


@ensure_not_bl
async def command_node(client: Client, message: Message) -> Optional[Message]:
    content = get_command_content(message)
    if not content:
        return await message.reply_text(NO_CODE, quote=False)
    return await run_node(content, message)
