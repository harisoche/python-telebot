from decouple import config

# Retrieve the bot token from the .env file
BOT_TOKEN = config('BOT_TOKEN')

# Check if the environment variable is set
if BOT_TOKEN is None:
    raise ValueError("BOT_TOKEN environment variable is not set. Please set it in the .env file.")