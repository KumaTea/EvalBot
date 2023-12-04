import logging
from pyrogram import filters
from handlers.functions import *
from common.data import LANG_CMDS
from handlers.edits import process_edited
from bot.session import eval_bot, scheduler
from handlers.callbacks import process_callback
from eval.tools import docker_clean, docker_pull
from pyrogram.handlers import MessageHandler, EditedMessageHandler , CallbackQueryHandler


def register_handlers():
    # group commands
    # langs
    eval_bot.add_handler(MessageHandler(command_bash, filters.command(LANG_CMDS['bash']) & filters.group))
    eval_bot.add_handler(MessageHandler(command_build, filters.command(LANG_CMDS['build']) & filters.group))
    eval_bot.add_handler(MessageHandler(command_node, filters.command(LANG_CMDS['node']) & filters.group))
    eval_bot.add_handler(MessageHandler(command_perl, filters.command(LANG_CMDS['perl']) & filters.group))
    eval_bot.add_handler(MessageHandler(command_ruby, filters.command(LANG_CMDS['ruby']) & filters.group))
    eval_bot.add_handler(MessageHandler(command_python, filters.command(LANG_CMDS['python']) & filters.group))
    eval_bot.add_handler(MessageHandler(command_busybox, filters.command(LANG_CMDS['busybox']) & filters.group))

    # others
    eval_bot.add_handler(MessageHandler(show_avail, filters.command(['avail', 'langs', 'support']) & filters.group))
    eval_bot.add_handler(MessageHandler(show_limit, filters.command(['limit']) & filters.group))

    # edited messages
    eval_bot.add_handler(EditedMessageHandler(process_edited, filters.group))

    # callbacks
    eval_bot.add_handler(CallbackQueryHandler(process_callback))

    return logging.info('[handlers.register register_handlers]\tHandlers registered')


def add_jobs():
    scheduler.add_job(docker_clean, 'cron', hour=4, minute=0)
    scheduler.add_job(docker_pull, 'cron', hour=2, minute=30)
    scheduler.start()
    return logging.info('[handlers.register manager]\tapscheduler started')
