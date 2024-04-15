
import json
from math import fabs
import requests
import sys
import subprocess
import importlib
from colorama import init, Fore, Back, Style
import time
from datetime import datetime
from pe_store import save_chat_record, read_chat_record

init()

REQUIRED_LIBRARIES = ['requests', 'colorama']

for library in REQUIRED_LIBRARIES:
    try:
        importlib.import_module(library)
    except ImportError:
        print(f"Installing {library} library...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", library])

# 这些值将通过 version.txt 文件读取
API_BASE = None
API_KEY = None
model_version = None
hacker_terminal_mode =False

conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."},
]

enable_background = False

def read_api_and_model_settings():
    global API_BASE, API_KEY, model_version
    try:
        with open('gpt/version.txt', 'r', encoding='utf-8') as file:
            settings = json.load(file)
            API_BASE = settings.get('api_base', API_BASE)
            API_KEY = settings.get('api_key', API_KEY)
            model_version = settings.get('model_version', model_version)
            print(f"Settings updated: Model Version - {model_version}, API Base - {API_BASE}, API Key - {API_KEY}")
    except FileNotFoundError:
        print("No 'version.txt' found. Please make sure it exists in the 'gpt' folder.")
    except json.JSONDecodeError:
        print("Error reading 'version.txt'. Please make sure it is in valid JSON format.")

def chat_with_gpt(input_text):
    global conversation_history, model_version, API_BASE, API_KEY
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    conversation_history.append({"role": "user", "content": input_text})
    data = {
        "model": model_version,
        "messages": conversation_history
    }
    response = requests.post(API_BASE, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    response_data = response.json()
    assistant_response = response_data['choices'][0]['message']['content']
    conversation_history.append(
        {"role": "assistant", "content": assistant_response})
    return assistant_response

def show_menu():
    print("=== Menu ===")
    print("1. Save chat record")
    print("2. Read chat record")
    print("3. Simulator Options")
    print("4. Quit")

def toggle_background():
    global enable_background
    enable_background = not enable_background
    print(f"Background is {'enabled' if enable_background else 'disabled'}.")

def simulator_menu():
    while True:
        print("\n=== Simulator Menu ===")
        print("1. Hacker Terminal Simulator")
        print("2. Regular Terminal Simulator")
        print("3. Back to Main Menu")
        sim_choice = input("Choose an option: ")
        if sim_choice == "1":
            toggle_hacker_mode()
        elif sim_choice == "2":
            print("Regular Terminal Simulator - This feature is not implemented yet.")
        elif sim_choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def toggle_hacker_mode():
    global hacker_terminal_mode
    hacker_terminal_mode = not hacker_terminal_mode
    if hacker_terminal_mode:
        try:
            with open('hck/hckcommand.txt', 'r', encoding='utf-8') as file:
                hck_command = file.read().strip()
            chat_with_gpt(hck_command)
            print("Hacker terminal mode is now activated.")
        except FileNotFoundError:
            print("Activation failed, please check if 'hck/hckcommand.txt' exists.")
            hacker_terminal_mode = False
    else:
        print("Hacker terminal mode is now deactivated.")

if __name__ == "__main__":
    # 读取 API 和模型设置
    read_api_and_model_settings()
    in_main = False
    while True:
        input_text = input("\cd me:")
        if input_text.lower() == "quit":
            break
        if input_text.lower() == "main":
            in_main = True
            show_menu()
        elif in_main:
            if input_text == "1":
                save_chat_record(conversation_history)
                print("Chat record saved successfully.")
            elif input_text == "2":
                read_chat_record()
            elif input_text == "3":
                simulator_menu()
            elif input_text == "4":
                in_main = False
            else:
                print("Invalid choice. Please try again.")
        else:
            if input_text.strip() == "":
                continue
            response_text = chat_with_gpt(input_text)
            response_text = "\cd robot: " + response_text
            for char in response_text:
                if enable_background:
                    sys.stdout.write(Back.WHITE + Fore.BLUE + char + Style.RESET_ALL)
                else:
                    sys.stdout.write(Fore.WHITE + char + Style.RESET_ALL)
                sys.stdout.flush()
                time.sleep(0.01)
            print()