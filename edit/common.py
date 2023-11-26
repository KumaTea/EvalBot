from edit.importer import *  # noqa
from typing import Optional
from bot.session import msg_store
from common.data import LANG_CMDS
from pyrogram.types import Message


def lang_detect(message: Message) -> Optional[str]:
    if message.text:
        text = message.text
        if message.text.startswith('/'):
            text = text[1:]
            for cmd in LANG_CMDS:
                if text.startswith(cmd):
                    return cmd
    return None


async def edited_process(message: Message) -> Optional[Message]:
    my_response = msg_store.get(message.chat.id, message.id)
    need_process = bool(my_response)
    if not need_process:
        return None

    lang = lang_detect(message)
    if not lang:
        return None

    command_name = f'run_{lang}'
    command = globals().get(command_name)
    if not command:
        return None

    return await command(message.text, message, edited=True, inform=my_response)
