import asyncio
import re
from typing import Tuple
import requests

from telethon import TelegramClient, events, utils
from telethon.tl import types
from telethon.tl.functions.messages import ExportChatInviteRequest

import hypercorn.asyncio

from hypercorn.asyncio import serve
from quart import Quart, render_template_string, request

from config import *
from misc import bot, logger
from keyboards import custom_keyboard
from keywords import *
from template import BASE_TEMPLATE

# Quart app
app = Quart(__name__)
app.secret_key = "SOME SECRET KEY HERE"

messageHistory = []

# авторизация в telethon
try:
    client = TelegramClient(TG_SESSION, TG_API_ID, TG_API_HASH)
except Exception as e:
    logger.error("Some error with auth")
    logger.exception(f"Exception {e}")

# hypercorn start handler
@app.before_serving
async def startup():
    sessions = []

    await client.start()
    await client.connect()

    me = await client.get_me()

    print(me.id, me.username)

    response = send_bot_msg(TG_BOT_TOKEN, "Бот успешно запущен...")
    if response != 200:
        error_msg = f"[БОТ]: Вероятно, что вы не запустили бота - @{bot_username}"
        logger.error(error_msg)
        await client.send_message(TG_ADMIN_ID, message=error_msg)


# hypercorn finish handler
@app.after_serving
async def shutdown():
    await client.disconnect()


# index route
@app.route("/", methods=["GET", "POST"])
async def root():
    content = "<h1>App is running...</h1>"
    return await render_template_string(BASE_TEMPLATE, content=content)


# получить юзернейм бота
def get_bot_username(token):
    r_query = f"https://api.telegram.org/bot{token}/getMe"

    response = requests.get(r_query)

    if response.status_code != 200:
        return response.json()

    return response.json()["result"]["username"]


# отправка сообщений через бота
def send_bot_msg(token, msg):
    r_query = (
        f"https://api.telegram.org/bot{token}/"
        f"sendMessage?chat_id={TG_ADMIN_ID}"
        f"&parse_mode=html"
        f"&text={msg}"
    )

    response = requests.get(r_query)
    print(response.text)
    return response.status_code


bot_username = get_bot_username(TG_BOT_TOKEN)


def find_keyword(word):
    return re.compile(rf"\b({word})\b", flags=re.IGNORECASE).search


def find_pair_keyword(pair: Tuple[str, str], message):
    if pair[0].lower() in message and pair[1].lower() in message:
        return True
    else:
        return False


# прослушивание новых сообщений
@client.on(events.NewMessage())
async def msg_handler(event):

    message = event.message.message
    found_words = [k for k in keywords if find_keyword(k)(message)]
    found_banned_pairs = [
        k for k in ban_pairs if find_pair_keyword(k, message.lower())]

    if len(found_banned_pairs) > 0:
        print("Banned pair found: ", found_banned_pairs)
        return

    if message in messageHistory:
        print("Duplicate message: ", message)
        return

    if found_words:
        print("Found words:", found_words, "in message:", event)

        chat = event.chat if event.chat else (await event.get_chat())
        chat_title = utils.get_display_name(chat)

        chat_username = None
        chat_link = None

        if isinstance(chat, types.Chat):
            try:
                chat_link = await client(ExportChatInviteRequest(chat.id))
                chat_link = chat_link.link
            except Exception as e:
                chat_link = None
                logger.info("Cannot get chat private link...")
                logger.exception(e)

        if isinstance(chat, types.Channel):
            chat_username = chat.username if chat.username else chat.id
        if isinstance(chat, types.User):
            chat_username = chat.username if chat.username else chat.id

        if chat_username == bot_username:
            return

        if chat_username:
            chat_msg_id = event.message.id

            if isinstance(chat_username, int):
                chat_link = f"t.me/c/{chat_username}/{chat_msg_id}"
                chat_username = None
            else:
                chat_link = f"t.me/{chat_username}/{chat_msg_id}"
                chat_username = f"@{chat_username}" if chat_username else None

        sender = await event.get_sender()

        if isinstance(sender, types.User):
            first_name = sender.first_name
            last_name = sender.last_name
            author_name = f"{first_name} {last_name}"

        else:
            author_name = f"{sender.title}"

        username = sender.username

        bot_msg_text = (
            f"<b>Чат:</b> {chat_title} ({chat_username})\n"
            f"<b>Автор:</b> {author_name} (@{username})\n"
            f"<b>Ссылка:</b> {chat_link}\n"
            f"<b>Сообщение:</b> {message}\n"
        )

        messageHistory.append(message)

        await bot.send_message(
            TG_ADMIN_ID,
            bot_msg_text,
            reply_markup=custom_keyboard(),
            disable_web_page_preview=True,
        )


if __name__ == "__main__":

    try:
        # client.loop.run_until_complete(serve(app, hypercorn.Config()))
        loop = client.loop
        asyncio.set_event_loop(loop)
        loop.run_until_complete(serve(app, hypercorn.Config()))

    except Exception as e:
        logger.error("Cannot run bot...")
        logger.exception(f"Exception: {e}")
