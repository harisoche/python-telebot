import logging
from telegram.ext import Application

from config import BOT_TOKEN
from handlers import start_handler, conv_add_data, conv_update_name, conv_update_age, show_data_handler

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    updater = Application.builder().token(BOT_TOKEN).build()

    # Add your handlers here
    updater.add_handler(start_handler)
    updater.add_handler(conv_add_data)
    updater.add_handler(conv_update_name)
    updater.add_handler(conv_update_age)
    updater.add_handler(show_data_handler)

    updater.run_polling()

if __name__ == '__main__':
    main()