import os

def get_file_path() -> str:
    os.makedirs('data', exist_ok=True)
    return 'data/user_message.txt'