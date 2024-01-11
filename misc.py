import sys
import logging

from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TG_BOT_TOKEN

bot = Bot(token=TG_BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

# logger
def get_logger():
	logger = logging.getLogger('bot')
	logger.setLevel(logging.DEBUG)
	file_handler = logging.FileHandler('app.log')
	stream_handler = logging.StreamHandler(stream=sys.stdout)

	file_handler.setLevel(logging.DEBUG)
	stream_handler.setLevel(logging.DEBUG)

	formatter = logging.Formatter('[%(levelname)s] - %(message)s')
	file_handler.setFormatter(formatter)
	stream_handler.setFormatter(formatter)

	logger.addHandler(file_handler)
	logger.addHandler(stream_handler)

	return logger

logger = get_logger()
