import os
import sys
import subprocess
import importlib
from colorama import init, Fore, Back, Style
import time
from datetime import datetime
from pe_store import save_chat_record, read_chat_record

init()  # 初始化 colorama 库

REQUIRED_LIBRARIES = ['requests', 'colorama']

for library in REQUIRED_LIBRARIES:
    try:
        importlib.import_module(library)
    except ImportError:
        print(f"Installing {library} library...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", library])

import requests
import json

API_BASE = 'https://api.closeai-asia.com/v1/chat/completions'
API_KEY = 'sk-kn8rVHdC8NlpjrWT8gfsQawK2USx8JWMIex1Midz1GK57Ib2'

conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."},
]

# 是否启用背景
enable_background = True

def chat_with_gpt(input_text):
    global conversation_history
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    conversation_history.append({"role": "user", "content": input_text})
    data = {
        "model": "gpt-3.5-turbo",
        "messages": conversation_history
    }
    response = requests.post(API_BASE, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    response_data = response.json()
    assistant_response = response_data['choices'][0]['message']['content']
    conversation_history.append({"role": "assistant", "content": assistant_response})

    return assistant_response


def show_menu():
    print("=== Menu ===")
    print("1. View API settings")
    print("2. Modify API settings")
    print("3. View AI output settings")
    print("4. Toggle background")
    print("5. Modify model version")
    print("6. Save chat record")
    print("7. Read chat record")
    print("8. Quit")


def view_api_settings():
    print("=== API Settings ===")
    print(f"API_BASE: {API_BASE}")
    print(f"API_KEY: {API_KEY}")


def modify_api_settings():
    global API_BASE, API_KEY
    print("=== Modify API Settings ===")
    new_api_base = input(f"Enter new API_BASE (current: {API_BASE}): ")
    new_api_key = input(f"Enter new API_KEY (current: {API_KEY}): ")
    if new_api_base.strip() != "":
        API_BASE = new_api_base
    if new_api_key.strip() != "":
        API_KEY = new_api_key
    print("API settings modified successfully.")


def view_ai_output_settings():
    print("=== AI Output Settings ===")
    print(f"Text color: {Fore.BLUE}")
    print(f"Background enabled: {enable_background}")
    print(f"Text speed: 0.01s per character")


def toggle_background():
    global enable_background
    enable_background = not enable_background
    print(f"Background is {'enabled' if enable_background else 'disabled'}.")


def modify_model_version():
    print("=== Modify Model Version ===")
    print("This feature is not implemented yet.")


if __name__ == "__main__":
    in_main = False  # 标记是否在主界面
    while True:
        input_text = input("/cd ")
        if input_text.lower() == "quit":
            break
        if input_text.lower() == "main":
            in_main = True
            show_menu()
        elif in_main:
            if input_text == "1":
                view_api_settings()
            elif input_text == "2":
                modify_api_settings()
            elif input_text == "3":
                view_ai_output_settings()
            elif input_text == "4":
                toggle_background()
            elif input_text == "5":
                modify_model_version()
            elif input_text == "6":
                save_chat_record(conversation_history)
                print("Chat record saved successfully.")
            elif input_text == "7":
                read_chat_record()
            elif input_text == "8":
                in_main = False
            else:
                print("Invalid choice. Please try again.")
        else:
            if input_text.strip() == "":
                continue
            response_text = chat_with_gpt(input_text)
            response_text = "/cd t " + response_text
            for char in response_text:
                if enable_background:
                    sys.stdout.write(Back.WHITE + Fore.BLUE + char + Style.RESET_ALL)
                else:
                    sys.stdout.write(Fore.BLUE + char + Style.RESET_ALL)
                sys.stdout.flush()
                time.sleep(0.01)
            print()
