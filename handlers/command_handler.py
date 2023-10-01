from utils import get_file_path
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

def update_data(chat_id, file_path, value, key):
    with open(file_path, "r+") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            parts = line.strip().split(":")
            if int(parts[0]) == chat_id:
                data = json.loads(":".join(parts[1:]))
                if key == "age":
                    data["age"] = value
                elif key == "name":
                    data["name"] = value

                updated_line = f"{chat_id}:{json.dumps(data)}\n"
                lines[i] = updated_line
                file.seek(0)
                file.writelines(lines)
                break

