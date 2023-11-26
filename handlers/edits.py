from typing import Optional
from pyrogram import Client
from pyrogram.types import Message
from edit.common import edited_process


async def process_edited(client: Client, message: Message) -> Optional[Message]:
    return await edited_process(message)
