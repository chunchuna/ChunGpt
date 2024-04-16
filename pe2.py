
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
hacker_terminal_mode = False
typewriter_effect = False
enable_background = False

conversation_history = [
    {"role": "system", "content": "I am a good robot for u"},
]


def read_api_and_model_settings():
    global API_BASE, API_KEY, model_version, typewriter_effect
    try:
        with open('gpt/version.txt', 'r', encoding='utf-8') as file:
            settings = json.load(file)
            API_BASE = settings.get('api_base', API_BASE)
            API_KEY = settings.get('api_key', API_KEY)
            model_version = settings.get('model_version', model_version)
            typewriter_effect = settings.get(
                'typewriter_effect', typewriter_effect)
            # print(
            # f"Settings updated: Model Version - {model_version}, API Base - {API_BASE}, API Key - {API_KEY}, Typewriter Effect - {typewriter_effect}")
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

    if hacker_terminal_mode:
        delay = read_hacker_mode_delay()
        time.sleep(delay)
    return assistant_response


def show_menu():
    print("=== Menu ===")
    print("1. Save chat record")
    print("2. Read chat record")
    print("3. Simulator Options")
    print("4. Quit")

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
            break
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
            # print("Hacker terminal mode is now activated.")
        except FileNotFoundError:
            print("Activation failed, please check if 'hck/hckcommand.txt' exists.")
            hacker_terminal_mode = False
    else:
        print("Hacker terminal mode is now deactivated.")


def read_hacker_mode_delay():
    try:
        with open('hck/hcktime.txt', 'r', encoding='utf-8') as file:
            delay = file.read().strip()
            return float(delay)
    except FileNotFoundError:
        print("No 'hck/hcktime.txt' found. Please make sure it exists in the 'hck' folder.")
        return 0.0  # Default delay
    except ValueError:
        print("'hck/hcktime.txt' should contain a single number, representing delay in seconds.")
        return 0.0  # Default delay


def read_hacker_mode_default():
    try:
        with open('hck/hckdefault.txt', 'r', encoding='utf-8') as file:
            default = file.read().strip().lower()
            return default == 'true'
    except FileNotFoundError:
        print(
            "No 'hck/hckdefault.txt' found. Please make sure it exists in the 'hck' folder.")
        return False  # Default setting
    except ValueError:
        print("'hck/hckdefault.txt' should contain either 'true' or 'false'.")
        return False  # Default setting

if __name__ == "__main__":
    # 读取 API 和模型设置
    read_api_and_model_settings()
    in_main = False
    # 默认启动黑客模式
    if read_hacker_mode_default():
        toggle_hacker_mode()
    while True:
        if hacker_terminal_mode:
            input_text = input(Fore.RED + "[chunchun@ru >^] :" + Style.RESET_ALL)
        else:
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
            response_text = Fore.GREEN + "[@ru.com >^] : " + Style.RESET_ALL + response_text
            if typewriter_effect:
                for char in response_text:
                    sys.stdout.write(char)
                    sys.stdout.flush()
                    time.sleep(0.01)
            else:
                sys.stdout.write(response_text)
                sys.stdout.flush()
            print()



