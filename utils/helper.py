import os
import json

def get_file_path() -> str:
    os.makedirs('data', exist_ok=True)
    return 'data/user_message.txt'

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

def find_data(chat_id, file_path):
    with open(file_path, "r+") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            parts = line.strip().split(":")
            if int(parts[0]) == chat_id:
                return json.loads(":".join(parts[1:]))

    return None

def is_valid_number(data):
    try:
        int(data)
        return True
    except ValueError:
        return False