import logging
from eval.tools import docker_clean
from handlers.register import register_handlers, add_jobs


def starting():
    docker_clean()
    register_handlers()
    add_jobs()

    return logging.info("[bot.starting starting]\tEvalBot Initialized.")
