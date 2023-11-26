from common.data import *
from pyrogram import Client
from typing import Callable
from pyrogram.types import Message
from func.runner import run, edit_run
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


async def edit_run_lang(
        code: str,
        message: Message,
        inform_id: int,
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
    return await edit_run(
        message=message,
        inform_id=inform_id,
        command=command,
        name=ct_name,
        image=image,
        code_file=filename,
    )


async def select_run_lang(
        edited: bool,
        code: str,
        message: Message,
        ct_name: str,
        image: str,
        filename: str,
        real_filename: str,
        create_lang_script: Callable,
        inform_id: int = None,
        script_executor: str = 'bash',
) -> Message:
    if edited:
        return await edit_run_lang(
            code=code,
            message=message,
            inform_id=inform_id,
            ct_name=ct_name,
            image=image,
            filename=filename,
            real_filename=real_filename,
            create_lang_script=create_lang_script,
            script_executor=script_executor,
        )
    else:
        return await run_lang(
            code=code,
            message=message,
            ct_name=ct_name,
            image=image,
            filename=filename,
            real_filename=real_filename,
            create_lang_script=create_lang_script,
            script_executor=script_executor,
        )


async def command_lang(client: Client, message: Message, run_lang_func: Callable) -> Message:
    content = get_command_content(message)
    if not content:
        return await message.reply_text(NO_CODE, quote=False)
    return await run_lang_func(content, message)
