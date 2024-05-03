import asyncio
import logging
import os
import sys


STORAGE_DIR = '/opt/tg_image_saver/storage/'
BOT_ADMIN = os.environ['BOT_ADMIN']
DELETE_TIMEOUT = 30


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
app_logger = logging.getLogger('app_logger')


async def delete_message(context, message, update):
    await asyncio.sleep(DELETE_TIMEOUT)
    await context.bot.deleteMessage(message_id = message.message_id, chat_id = update.message.chat_id)


def calc_bytes(size_in_bytes):
    suffixes = ['B', 'KB', 'MB', 'GB']
    index = 0
    while size_in_bytes >= 1024 and index < len(suffixes) - 1:
        size_in_bytes /= 1024.0
        index += 1
    return f"{size_in_bytes:.2f}{suffixes[index]}"
