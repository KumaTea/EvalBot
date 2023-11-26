from edit.importer import *  # noqa
from typing import Optional
from bot.session import msg_store
from common.data import LANG_CMDS
from pyrogram.types import Message
from bot.tools import get_command_content


def lang_detect(message: Message) -> Optional[str]:
    if message.text:
        text = message.text
        if message.text.startswith('/'):
            text = text[1:]
            for lang in LANG_CMDS:
                for cmd in LANG_CMDS[lang]:
                    if text.startswith(cmd):
                        return lang
    return None


async def edited_process(message: Message) -> Optional[Message]:
    my_response = msg_store.get(message.chat.id, message.id)
    if my_response is None:
        return None

    lang = lang_detect(message)
    if not lang:
        return None

    command_name = f'run_{lang}'
    command = globals().get(command_name)
    if not command:
        return None

    code = get_command_content(message)
    return await command(code, message, edited=True, inform=my_response)
