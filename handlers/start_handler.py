from telegram.ext import CommandHandler

async def start(update, context):
    user = update.message.from_user
    await context.bot.send_message(chat_id=update.message.chat_id, text=f"Hello, {user.first_name}! This is your bot. Use /help for more options.")

start_handler = CommandHandler('start', start)