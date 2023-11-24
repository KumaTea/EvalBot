import logging
from pyrogram import filters
from bot.session import eval_bot
from handlers.functions import *
from common.data import LANG_CMDS
from handlers.callbacks import process_callback
from pyrogram.handlers import MessageHandler, CallbackQueryHandler


def register_handlers():
    # group commands
    # langs
    eval_bot.add_handler(MessageHandler(command_bash, filters.command(LANG_CMDS['bash']) & filters.group))
    eval_bot.add_handler(MessageHandler(command_node, filters.command(LANG_CMDS['node']) & filters.group))
    eval_bot.add_handler(MessageHandler(command_python, filters.command(LANG_CMDS['python']) & filters.group))
    eval_bot.add_handler(MessageHandler(command_busybox, filters.command(LANG_CMDS['busybox']) & filters.group))

    # others
    eval_bot.add_handler(MessageHandler(show_avail, filters.command(['avail', 'langs', 'support']) & filters.group))
    eval_bot.add_handler(MessageHandler(show_limit, filters.command(['limit']) & filters.group))

    # callbacks
    # eval_bot.add_handler(CallbackQueryHandler(process_callback))

    return logging.info('Registered handlers')


# def manager():
#     scheduler = session.scheduler
#     scheduler.add_job(func, 'cron', [arg1], hour=4)
#     return logging.info('Scheduler started')
