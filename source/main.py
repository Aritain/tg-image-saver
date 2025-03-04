import logging
import os

from app.handlers import (
    clear_context_data,
    error_handler,
    get_random,
    save_image,
    stats,
)
from app.helpers import (
    app_logger,
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)
logging.getLogger("httpx").setLevel(logging.WARNING)


def main():
    app_logger.info('Starting Bot...')
    bot = Application.builder().token(os.environ['TG_TOKEN']).build()

    bot.add_handler(CommandHandler("get_random", get_random))
    bot.add_handler(CommandHandler("stats", stats))
    bot.add_handler(MessageHandler(filters.PHOTO, save_image))
    bot.add_error_handler(error_handler)

    job_queue = bot.job_queue
    job_queue.run_repeating(clear_context_data, interval=1800, first=0)

    bot.run_polling()


if __name__ == "__main__":
    main()
