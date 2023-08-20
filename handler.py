import asyncio
import json
import os

from redis import ConnectionPool
from redis import Redis
from telegram import Update
from telegram.ext import Application
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler
from telegram.ext import filters

redis_pool = ConnectionPool.from_url(os.environ["REDIS_DSN"])
redis = Redis(connection_pool=redis_pool)

application = (
    Application.builder().token(os.environ["TELEGRAM_TOKEN"]).updater(None).build()
)


async def on_enter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi!")
    # set redis key
    # send captcha


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Catch it")
    # look on redis, if present, delete any message


async def on_leave(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bye")
    # remove the key from redis


application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_enter))
application.add_handler(MessageHandler(filters.CHAT & ~filters.COMMAND, on_message))
application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, on_leave))


async def main(event):
    async with application:
        await application.process_update(
            Update.de_json(json.loads(event["body"]), application.bot)
        )


def telegram(event, context):
    asyncio.run(main(event))

    return {
        "statusCode": 200,
    }
