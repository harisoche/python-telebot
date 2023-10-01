import logging
from telegram.ext import Application

from config import BOT_TOKEN
from handlers import start_handler, echo_handlers, new_data_handler, update_name_handler, update_age_handler

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    updater = Application.builder().token(BOT_TOKEN).build()

    # Add your handlers here
    updater.add_handler(start_handler)
    updater.add_handler(echo_handlers)
    updater.add_handler(new_data_handler)
    updater.add_handler(update_name_handler)
    updater.add_handler(update_age_handler)

    updater.run_polling()
    # updater.idle()

if __name__ == '__main__':
    main()