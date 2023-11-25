from common.data import *
from pyrogram import Client
from func.runner import run
from typing import Callable
from pyrogram.types import Message
from bot.tools import get_command_content


async def run_lang(
        code: str,
        message: Message,
        ct_name: str,
        image: str,
        filename: str,
        real_filename: str,
        create_lang_script: Callable,
        script_executor: str = 'bash',
) -> Message:
    os.mkdir(f'{SHM}/{ct_name}')
    with open(real_filename, 'w', encoding='utf-8') as f:
        f.write(code)
    script_file = create_lang_script(ct_name, filename)
    command = f'{script_executor} {script_file}'
    return await run(
        message=message,
        command=command,
        name=ct_name,
        image=image,
        code_file=filename,
    )


async def command_lang(client: Client, message: Message, run_lang_func: Callable) -> Message:
    content = get_command_content(message)
    if not content:
        return await message.reply_text(NO_CODE, quote=False)
    return await run_lang_func(content, message)
