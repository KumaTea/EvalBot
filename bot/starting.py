import logging
from eval.tools import startup_clean
from handlers.register import register_handlers


def starting():
    startup_clean()
    register_handlers()

    return logging.info("[EvalBot] Initialized.")
