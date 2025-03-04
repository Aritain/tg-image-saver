import asyncio
import random
import string
import time
import os
import os.path

from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from .helpers import (
    app_logger,
    calc_bytes,
    delete_message,
    BOT_ADMIN,
    STORAGE_DIR,
)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Get local storage stats:
    1. Number of files
    2. Total size of storage
    """
    if update.message.chat.id != int(BOT_ADMIN):
        return

    # Delete user command
    await context.bot.deleteMessage(message_id=update.message.id, chat_id=update.message.chat_id)
    file_count = len(os.listdir(STORAGE_DIR))
    dir_size = sum(d.stat().st_size for d in os.scandir(STORAGE_DIR) if d.is_file())
    dir_size = calc_bytes(dir_size)
    message = await update.message.reply_text(
        f'Currently there are {file_count} files, total size is {dir_size}'
    )

    # Delete sent image after some timeout
    asyncio.create_task(delete_message(context, message, update))


async def save_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Receive image from user & save it locally in storage directory
    """
    if update.message.chat.id != int(BOT_ADMIN):
        return

    # Delete user image
    await context.bot.deleteMessage(message_id=update.message.id, chat_id=update.message.chat_id)
    new_file = await update.message.effective_attachment[-1].get_file()
    # Generate random string line with len == 8
    filename = ''.join(random.choices(string.ascii_letters, k=8))
    # Add epoch time to filename
    filename += f'_{str(int(time.time()))}.jpg'
    app_logger.info('Downloading %s of %s size', filename, new_file.file_size)
    await new_file.download_to_drive(f'{STORAGE_DIR}{filename}')
    message = await update.message.reply_text('Image saved')

    # Delete sent image after some timeout
    asyncio.create_task(delete_message(context, message, update))


async def get_random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Send random image from storage to user
    """
    user_id = update.message.chat.id
    if user_id != int(BOT_ADMIN):
        return

    # Delete user command
    await context.bot.deleteMessage(message_id=update.message.id, chat_id=update.message.chat_id)

    # Get random file and write it to 'cache' to prevent same files to be sent over and over
    files = os.listdir(STORAGE_DIR)
    file_count = len(files)
    if user_id in context.user_data:
        files = [file for file in files if file not in context.user_data[user_id]]
    chosen_file = random.choice(files)
    if user_id not in context.user_data:
        context.user_data[user_id] = []
    context.user_data[user_id].append(chosen_file)
    if len(context.user_data[user_id]) == file_count:
        context.user_data[user_id] = []

    message = await context.bot.send_photo(
        chat_id=user_id,
        photo=f'{STORAGE_DIR}{chosen_file}'
    )

    # Delete sent image after some timeout
    asyncio.create_task(delete_message(context, message, update))


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    app_logger.error("Exception while handling an update: %s", context.error)
    await asyncio.sleep(0)


def clear_context_data(context: CallbackContext):
    context.user_data.clear()
