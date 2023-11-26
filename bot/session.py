import logging
import configparser
from pyrogram import Client
from bot.store import MsgStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

config = configparser.ConfigParser()
config.read('config.ini')
eval_bot = Client(
    'eval',
    api_id=config['eval']['api_id'],
    api_hash=config['eval']['api_hash'],
    bot_token=config['eval']['bot_token'],
)

scheduler = AsyncIOScheduler()

msg_store = MsgStore()
