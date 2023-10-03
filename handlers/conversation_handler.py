from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, CallbackContext, filters
from telegram import Update
import json
from utils import get_file_path, update_data, is_valid_number

NAME, AGE = range(2)

async def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    context.user_data['attempts'] = 0
    await update.message.reply_text(f"Hello, {user.first_name}! Please enter your name:")
    return NAME

async def receive_name(update: Update, context: CallbackContext) -> int:
    name = update.message.text

    if name.strip():
        context.user_data['name'] = name
        await update.message.reply_text(f"Thanks, {context.user_data['name']}! Now, please enter your age:")
        return AGE
    else:
        await update.message.reply_text("Name cannot be empty. Please enter your name again.")
        context.user_data['attempts'] += 1
        if context.user_data['attempts'] >= 3:
            await update.message.reply_text("You've exceeded the maximum attempts. Conversation canceled.")
            return ConversationHandler.END
        return NAME

async def receive_age(update: Update, context: CallbackContext) -> int:
    age = update.message.text

    if is_valid_number(age):
        context.user_data['age'] = age
        data = {
            "name": context.user_data['name'],
            "age": int(context.user_data['age'])
        }

        message_to_write = f"{update.message.chat_id}:{json.dumps(data)}\n"

        file_path = get_file_path()

        with open(file_path, 'a') as f:
            f.write(message_to_write)

        await update.message.reply_text(f"Thanks you! Your data: name {context.user_data['name']} and age {context.user_data['age']}")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Age must be a number. Please enter your age again.")
        context.user_data['attempts'] += 1
        if context.user_data['attempts'] >= 3:
            await update.message.reply_text("You've exceeded the maximum attempts. Conversation canceled.")
            return ConversationHandler.END
        return AGE

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("You have canceled the conversation.")
    return ConversationHandler.END

conv_add_data = ConversationHandler(
        entry_points=[CommandHandler('add_data', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_age)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

async def update_name(update: Update, context: CallbackContext):
    context.user_data['attempts'] = 0
    await update.message.reply_text(f"Please enter name:")
    return NAME

async def get_update_name(update: Update, context: CallbackContext):
    file_path = get_file_path()
    user_id = update.message.chat_id
    text = update.message.text.strip()
    update_data(user_id, file_path, text, "name")
    await update.message.reply_text(f"Name updated to {text}")
    return ConversationHandler.END

conv_update_name = ConversationHandler(
        entry_points=[CommandHandler('update_name', update_name)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_update_name)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

async def update_age(update: Update, context: CallbackContext):
    context.user_data['attempts'] = 0
    await update.message.reply_text(f"Please enter age:")
    return AGE

async def get_update_age(update: Update, context: CallbackContext):
    file_path = get_file_path()
    user_id = update.message.chat_id
    age = update.message.text
    if is_valid_number(age):
        update_data(user_id, file_path, age, "age")
        await update.message.reply_text(f"Age updated to {age}")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Age must be a number. Please enter your age again.")
        context.user_data['attempts'] += 1
        if context.user_data['attempts'] >= 3:
            await update.message.reply_text("You've exceeded the maximum attempts. Conversation canceled.")
            return ConversationHandler.END
        return AGE

conv_update_age = ConversationHandler(
        entry_points=[CommandHandler('update_age', update_age)],
        states={
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_update_age)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )