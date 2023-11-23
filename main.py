from common.data import debug_mode

if not debug_mode:
    import uvloop
    uvloop.install()

from bot.session import eval_bot
from bot.starting import starting


starting()


if __name__ == '__main__':
    eval_bot.run()
