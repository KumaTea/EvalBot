from common.data import *
from pyrogram import Client
from pyrogram.types import Message
from bot.auth import ensure_not_bl


@ensure_not_bl
async def show_limit(client: Client, message: Message) -> Message:
    chat_id = message.chat.id
    trusted = chat_id in trusted_group
    limits = TRUSTED_LIMITS if trusted else DOCKER_LIMITS
    text = '```\n'
    text += f"CPU: {limits['cpu']}\n"
    text += f"MEM: {limits['memory'] / MiB}MB\n"
    text += f"SHM: {limits['shm_size'] / MiB}MB\n"
    text += f"TME: {limits['timeout']}s\n"
    text += f"R/W: {not limits['read_only']}\n"
    text += f"NET: {not limits['no_net']}\n"
    text += '```'
    return await message.reply_text(text, quote=False)
