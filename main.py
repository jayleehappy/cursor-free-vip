# main.py
# This script allows the user to choose which script to run.
import os
import sys
import json
from logo import print_logo
from colorama import Fore, Style, init
from cursor_register import CursorRegistration
from reset_machine_manual import MachineIDResetter
from quit_cursor import quit_cursor
from language import Language

# 初始化colorama
init()

# 定义emoji和颜色常量
EMOJI = {
    "FILE": "📄",
    "BACKUP": "💾",
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "RESET": "🔄",
    "MENU": "📋",
    "ARROW": "➜",
    "LANG": "🌐"
}

class Translator:
    def __init__(self):
        self.current_language = 'zh_tw'  # 默认语言
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """加载所有可用的翻译"""
        locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
        if hasattr(sys, '_MEIPASS'):
            locales_dir = os.path.join(sys._MEIPASS, 'locales')
            
        for file in os.listdir(locales_dir):
            if file.endswith('.json'):
                lang_code = file[:-5]  # 移除 .json
                with open(os.path.join(locales_dir, file), 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
    
    def get(self, key, **kwargs):
        """获取翻译文本"""
        try:
            keys = key.split('.')
            value = self.translations.get(self.current_language, {})
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k, key)
                else:
                    return key  # 如果中間值不是字典，返回原始key
            return value.format(**kwargs) if kwargs else value
        except Exception:
            return key  # 出現任何錯誤時返回原始key
    
    def set_language(self, lang_code):
        """设置当前语言"""
        if lang_code in self.translations:
            self.current_language = lang_code
            return True
        return False

# 创建翻译器实例
translator = Translator()

def print_menu():
    """打印菜单选项"""
    print(f"\n{Fore.CYAN}{EMOJI['MENU']} {translator.get('menu.title')}:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'─' * 40}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}0{Style.RESET_ALL}. {EMOJI['ERROR']} {translator.get('menu.exit')}")
    print(f"{Fore.GREEN}1{Style.RESET_ALL}. {EMOJI['RESET']} {translator.get('menu.reset')}")
    print(f"{Fore.GREEN}2{Style.RESET_ALL}. {EMOJI['SUCCESS']} {translator.get('menu.register')}")
    print(f"{Fore.GREEN}3{Style.RESET_ALL}. {EMOJI['ERROR']} {translator.get('menu.quit')}")
    print(f"{Fore.GREEN}4{Style.RESET_ALL}. {EMOJI['LANG']} {translator.get('menu.select_language')}")
    print(f"{Fore.YELLOW}{'─' * 40}{Style.RESET_ALL}")

def select_language():
    """语言选择菜单"""
    print(f"\n{Fore.CYAN}{EMOJI['LANG']} {translator.get('menu.select_language')}:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'─' * 40}{Style.RESET_ALL}")
    
    languages = translator.get('languages')
    for i, (code, name) in enumerate(languages.items()):
        print(f"{Fore.GREEN}{i}{Style.RESET_ALL}. {name}")
    
    try:
        choice = input(f"\n{EMOJI['ARROW']} {Fore.CYAN}{translator.get('menu.input_choice', choices='0-' + str(len(languages)-1))}: {Style.RESET_ALL}")
        if choice.isdigit() and 0 <= int(choice) < len(languages):
            lang_code = list(languages.keys())[int(choice)]
            translator.set_language(lang_code)
            return True
    except (ValueError, IndexError):
        pass
    
    print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('menu.invalid_choice')}{Style.RESET_ALL}")
    return False

def main():
    # 打印 Logo
    print_logo()
    
    # 打印修改者信息
    print(f"\n{Fore.CYAN}Modified by: {Fore.GREEN}jayleehappy{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Project URL: {Fore.GREEN}https://github.com/jayleehappy/cursor-free-vip{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Original Project: {Fore.GREEN}https://github.com/yeongpin/cursor-free-vip{Style.RESET_ALL}\n")
    
    # 初始化语言
    lang = Language()
    translator = lang.get_translator()
    
    # 显示菜单
    while True:
        try:
            print(f"\n{Fore.CYAN}=== {translator.get('main.menu')} ==={Style.RESET_ALL}")
            print(f"{Fore.WHITE}1. {translator.get('main.register_cursor')}")
            print(f"2. {translator.get('main.reset_machine')}")
            print(f"3. {translator.get('main.quit_cursor')}")
            print(f"4. {translator.get('main.exit')}")
            
            choice = input(f"\n{translator.get('main.enter_choice')}: ")
            
            if choice == "1":
                registration = CursorRegistration(translator)
                if registration.setup_email():
                    registration.register_cursor()
            elif choice == "2":
                resetter = MachineIDResetter(translator)
                resetter.reset()
            elif choice == "3":
                quit_cursor(translator)
            elif choice == "4":
                print(f"\n{Fore.GREEN}{translator.get('main.goodbye')}{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(f"\n{Fore.RED}{translator.get('main.invalid_choice')}{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}{translator.get('main.exit_warning')}{Style.RESET_ALL}")
            try:
                confirm = input(f"{translator.get('main.confirm_exit')} (Y/N): ").lower()
                if confirm == 'y':
                    print(f"\n{Fore.GREEN}{translator.get('main.goodbye')}{Style.RESET_ALL}")
                    sys.exit(0)
            except KeyboardInterrupt:
                continue
        except Exception as e:
            print(f"\n{Fore.RED}{translator.get('main.error', error=str(e))}{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 