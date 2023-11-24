from common.data import *
from pyrogram import Client
from pyrogram.types import Message
from bot.auth import ensure_not_bl


@ensure_not_bl
async def show_avail(client: Client, message: Message) -> Message:
    text = 'Available languages:\n'
    for image in LANG_CMDS:
        text += f'{image}: `{LANG_CMDS[image][1]}`\n'
    return await message.reply_text(text, quote=False)
