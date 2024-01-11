""" keyboards """
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# inline keyboards
def custom_keyboard():
	ticket_updated_btn = InlineKeyboardButton('👌', callback_data='ticket_updated')
	ticket_notneed_btn = InlineKeyboardButton('🤷', callback_data='ticket_notneed')
	ticket_out_btn = InlineKeyboardButton('👨‍💻', callback_data='ticket_our')

	keyboard = InlineKeyboardMarkup(row_width=3)
	keyboard.row(ticket_updated_btn, ticket_notneed_btn, ticket_out_btn)

	return keyboard

def ticket_updated_keyboard():
	keyboard = InlineKeyboardMarkup(row_width=1)
	button = InlineKeyboardButton('Тикет обработан 👌', callback_data='ok')
	keyboard.row(button)

	return keyboard

def ticket_notneed_keyboard():
	keyboard = InlineKeyboardMarkup(row_width=1)
	button = InlineKeyboardButton('Не требует обработки 🤷', callback_data='ok')
	keyboard.row(button)

	return keyboard

def ticket_our_keyboard():
	keyboard = InlineKeyboardMarkup(row_width=3)
	button = InlineKeyboardButton('Наш 👨‍💻', callback_data='ok')
	keyboard.row(button)

	return keyboard