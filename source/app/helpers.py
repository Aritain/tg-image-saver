import logging
import os
import sys

STORAGE_DIR = '/opt/tg_image_saver/storage/'
BOT_ADMIN = os.environ['BOT_ADMIN']

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
app_logger = logging.getLogger('app_logger')
