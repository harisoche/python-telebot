from telegram.ext import MessageHandler, filters

async def echo(update, context):
    user_message = update.message.text
    await context.bot.send_message(chat_id=update.message.chat_id, text=f"You said: {user_message}")

echo_handlers = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)