import logging
from eval.tools import docker_clean, docker_pull
from handlers.register import register_handlers, add_jobs


def starting():
    register_handlers()
    add_jobs()

    return logging.info("[bot.starting starting]\tEvalBot Initialized.")
