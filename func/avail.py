from common.data import *
from pyrogram import Client
from share.auth import ensure_auth
from pyrogram.types import Message


@ensure_auth
async def show_avail(client: Client, message: Message) -> Message:
    text = 'Available languages:\n'
    for image in LANG_CMDS:
        if len(LANG_CMDS[image]) > 1:
            alias = LANG_CMDS[image][1]
        else:
            alias = LANG_CMDS[image][0]
        text += f'{image}: `/{alias}`\n'
    return await message.reply_text(text, quote=False)
