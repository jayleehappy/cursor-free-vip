import os
import time
import random
from colorama import Fore, Style, init
from browser import BrowserManager
from control import BrowserControl
from quit_cursor import quit_cursor
import subprocess
import sys

# 初始化 colorama
init()

# 定义 emoji 常量
EMOJI = {
    'START': '🚀',
    'PROCESS': '🔄',
    'SUCCESS': '✅',
    'ERROR': '❌',
    'INFO': 'ℹ️',
    'WAIT': '⏳'
}

class CursorSwitch:
    def __init__(self, translator=None):
        self.translator = translator
        self.settings_url = "https://www.cursor.com/settings"
        self.browser = None
        self.browser_manager = None
        
    def switch_account(self):
        """切换 Cursor 账号"""
        try:
            print(f"{Fore.CYAN}{EMOJI['START']} {self.translator.get('switch.start_process')}...{Style.RESET_ALL}")
            
            # 退出当前 Cursor
            self._quit_cursor()
            
            # 清理浏览器数据
            self._clear_browser_data()
            
            # 重启 Cursor
            self._restart_cursor()
            
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('switch.account_switch_complete')}...{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('switch.process_error', error=str(e))}{Style.RESET_ALL}")
            return False
            
    def _quit_cursor(self):
        """退出 Cursor"""
        try:
            print(f"{Fore.CYAN}{EMOJI['PROCESS']} {self.translator.get('switch.quitting_cursor')}...{Style.RESET_ALL}")
            quit_cursor()
            time.sleep(2)  # 等待进程完全退出
            return True
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('switch.quit_error', error=str(e))}{Style.RESET_ALL}")
            return False
            
    def _clear_browser_data(self):
        """清理浏览器数据"""
        try:
            print(f"{Fore.CYAN}{EMOJI['PROCESS']} {self.translator.get('switch.clearing_browser_data')}...{Style.RESET_ALL}")
            
            # 初始化浏览器
            self.browser_manager = BrowserManager()
            self.browser = self.browser_manager.init_browser()
            
            # 访问设置页面
            self.browser.get(self.settings_url)
            time.sleep(2)
            
            # 点击退出登录按钮
            logout_button = self.browser.ele("@data-testid=logout")
            if logout_button:
                logout_button.click()
                time.sleep(2)
                
            # 关闭浏览器
            if self.browser_manager:
                self.browser_manager.quit()
                
            return True
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('switch.clear_data_error', error=str(e))}{Style.RESET_ALL}")
            return False
            
    def _restart_cursor(self):
        """重启 Cursor"""
        try:
            print(f"{Fore.CYAN}{EMOJI['PROCESS']} {self.translator.get('switch.restarting_cursor')}...{Style.RESET_ALL}")
            
            # 获取 Cursor 安装路径
            cursor_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'Cursor', 'Cursor.exe')
            
            if not os.path.exists(cursor_path):
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('switch.cursor_not_found')}...{Style.RESET_ALL}")
                return False
                
            # 启动 Cursor
            subprocess.Popen([cursor_path])
            time.sleep(5)  # 等待 Cursor 启动
            
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('switch.cursor_restarted')}...{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('switch.restart_error', error=str(e))}{Style.RESET_ALL}")
            return False 