from pyrogram import Client
from bot.auth import ensure_not_bl
from pyrogram.types import CallbackQuery


@ensure_not_bl
async def process_callback(client: Client, callback_query: CallbackQuery):
    task = callback_query.data.split('_')[0]
    # if task == 'poll':
    #     return await poll_callback_handler(client, callback_query)
    return await callback_query.answer(task, show_alert=True)
