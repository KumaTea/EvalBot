import logging
from pyrogram import filters
from bot.session import eval_bot
from handlers.functions import *
from handlers.callbacks import process_callback
from pyrogram.handlers import MessageHandler, CallbackQueryHandler


def register_handlers():
    # group commands
    eval_bot.add_handler(MessageHandler(command_python, filters.command(['py', 'python', 'python3']) & filters.group))
    eval_bot.add_handler(MessageHandler(command_bash, filters.command(['sh', 'bash']) & filters.group))

    # callbacks
    # eval_bot.add_handler(CallbackQueryHandler(process_callback))

    return logging.info('Registered handlers')


# def manager():
#     scheduler = session.scheduler
#     scheduler.add_job(func, 'cron', [arg1], hour=4)
#     return logging.info('Scheduler started')
