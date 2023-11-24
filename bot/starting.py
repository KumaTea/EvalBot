import logging
from eval.tools import startup_clean, pull_all
from handlers.register import register_handlers


def starting():
    pull_all()
    startup_clean()
    register_handlers()

    return logging.info("[EvalBot] Initialized.")
