import uuid
from typing import Optional
from pyrogram.types import Message


def get_command_content(message: Message) -> Optional[str]:
    """
    Remove /cmd of a message,
    or get its replied message.
    Message must start with '/'.
    """
    text = message.text
    if not text:
        return None

    command_entity = message.entities[0]
    if len(text) > command_entity.length:
        text = text[command_entity.length+1:]
        return text

    reply = message.reply_to_message
    if reply:
        return reply.text

    return None


def gen_uuid(length: int = 4) -> str:
    """
    Generate a random UUID string.
    :param length: The length of the UUID string.
    :return: A random UUID string.
    """
    return str(uuid.uuid4())[:length]
