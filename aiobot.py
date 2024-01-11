from aiogram import types
from aiogram.utils import executor

from aiogram.dispatcher.webhook import EditMessageReplyMarkup

from misc import bot, dp, logger
from keyboards import *

# command for testing
@dp.message_handler(commands=['test'])
async def process_message(message: types.Message):
	await message.answer('Бот успешно работает...', reply_markup=custom_keyboard())

# inline keyboard handler
@dp.callback_query_handler()
async def process_inline_keyboard(query: types.CallbackQuery):
	try:
		chat_id = query['message']['chat']['id']
		message_id = query['message']['message_id']

		if query.data == 'ticket_updated':
			return EditMessageReplyMarkup(chat_id, message_id, reply_markup=ticket_updated_keyboard())

		if query.data == 'ticket_notneed':
			return EditMessageReplyMarkup(chat_id, message_id, reply_markup=ticket_notneed_keyboard())

		if query.data == 'ticket_our':
			return EditMessageReplyMarkup(chat_id, message_id, reply_markup=ticket_our_keyboard())

	except:
		logger.error('Cannot process inline keyboard')
		logger.exception(f'Exception: {e}')	
	
def run():
	try:
		executor.start_polling(dp, skip_updates=True)
	except Exception as e:
		logger.error('Bot cannot be run...')
		logger.exception(f'Exception: {e}')

if __name__ == '__main__':
	run()