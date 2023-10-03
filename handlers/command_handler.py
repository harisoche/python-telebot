from utils import get_file_path, update_data, find_data
from telegram.ext import CommandHandler, CallbackContext
from telegram import Update
import json

async def new_data(update: Update, context: CallbackContext):
    user_message = context.args

    if user_message:
        user_id = update.message.chat_id
        if "name" not in user_message or "age" not in user_message:
            return await context.bot.send_message(chat_id=user_id, text="Invalid format. Please use: /new_data name [name1] [name2] ... and age [age]")

        names = user_message[user_message.index("name") + 1:user_message.index("age")]
        age = user_message[user_message.index("age") + 1:]

        if not names or not age:
            return await context.bot.send_message(chat_id=user_id, text="Invalid format. Please provide at least one name and an age.")

        names_str = " ".join(names)
        data = {
            "name": names_str,
            "age": int(age[0])
        }

        message_to_write = f"{user_id}:{json.dumps(data)}\n"

        file_path = get_file_path()

        with open(file_path, 'a') as f:
            f.write(message_to_write)

        await context.bot.send_message(chat_id=user_id, text=f"New data received: Names - {names_str}, Age - {age[0]}")
    else:
        await context.bot.send_message(chat_id=user_id, text="Please provide a message to write to the file.")

new_data_handler = CommandHandler('new_data', new_data)

async def update_name(update: Update, context: CallbackContext):
    file_path = get_file_path()
    user_id = update.message.chat_id
    text = update.message.text.split("/update_name")[1].strip()
    update_data(user_id, file_path, text, "name")
    await context.bot.send_message(chat_id=user_id, text=f"Name updated to {text}")

update_name_handler = CommandHandler('update_name', update_name, has_args=True)

async def update_age(update: Update, context: CallbackContext):
    file_path = get_file_path()
    user_id = update.message.chat_id
    text = update.message.text.split("/update_age")[1].strip()
    update_data(user_id, file_path, text, "age")
    await context.bot.send_message(chat_id=user_id, text=f"Age updated to {text}")

update_age_handler = CommandHandler('update_age', update_age, has_args=True)

async def show_data(update: Update, context: CallbackContext):
    file_path = get_file_path()
    user_id = update.message.chat_id
    data = find_data(user_id, file_path)
    if data is not None:
        return await update.message.reply_text(f"Your data: name {data['name']} and age {data['age']}")

    await update.message.reply_text("No data found.")

show_data_handler = CommandHandler('show_data', show_data)