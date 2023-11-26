from pyrogram import Client
from pyrogram.types import CallbackQuery


def format_ram_usage(mem_usage: int) -> str:
    if mem_usage < 1024:
        return f'{mem_usage} KB'
    elif mem_usage < 1024 * 1024:
        return f'{mem_usage / 1024:.3f} MB'
    else:
        return f'{mem_usage / 1024 / 1024:.3f} GB'


async def callback_show_stat(client: Client, callback_query: CallbackQuery) -> tuple:
    task, used_time, peak_mem_hex, exit_code_hex = callback_query.data.split('_')
    result = 'Statistics:\n\n'

    result += f'Used Time: {used_time}\n'

    if peak_mem_hex != '?':
        peak_mem = int(peak_mem_hex, 16)
        result += f'Peak Memory: {format_ram_usage(peak_mem)}\n'
    else:
        result += 'Peak Memory: ?\n'

    if exit_code_hex != '?':
        exit_code = int(exit_code_hex, 16)
        result += f'Exit Code: {exit_code} '
        if exit_code == 0:
            result += '(OK)'
        else:
            result += '(ERROR)'
    else:
        result += 'Exit Code: ? (ERROR)'

    return await callback_query.answer(result, show_alert=True)
