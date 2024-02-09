from pyrogram import Client
from bot.auth import ensure_auth
from pyrogram.types import CallbackQuery
from func.stat import callback_show_stat


@ensure_auth
async def process_callback(client: Client, callback_query: CallbackQuery):
    task = callback_query.data.split('_')[0]
    if task == 'stat':
        return await callback_show_stat(client, callback_query)
    return await callback_query.answer('未知按钮', show_alert=True)
