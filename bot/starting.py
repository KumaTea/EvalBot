import logging
from handlers.register import register_handlers


def starting():
    register_handlers()

    return logging.info("[EvalBot] Initialized.")
