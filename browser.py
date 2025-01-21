from DrissionPage import ChromiumOptions, ChromiumPage
import sys
import os
import logging
import shutil
import tempfile
from colorama import Fore, Style, init

# 初始化colorama
init()

class BrowserManager:
    def __init__(self, noheader=False):
        self.browser = None
        self.noheader = noheader
        self.user_data_dir = None

    def init_browser(self):
        """初始化浏览器"""
        co = self._get_browser_options()
        
        # 强制设置为显式模式
        os.environ['BROWSER_HEADLESS'] = 'False'
        
        # 清理并设置新的用户数据目录
        self._setup_user_data_dir()
        
        self.browser = ChromiumPage(co)
        return self.browser

    def _setup_user_data_dir(self):
        """设置并清理用户数据目录"""
        try:
            # 在临时目录创建新的用户数据目录
            temp_dir = tempfile.gettempdir()
            self.user_data_dir = os.path.join(temp_dir, f'cursor_chrome_data_{os.getpid()}')
            
            # 如果目录已存在，先删除
            if os.path.exists(self.user_data_dir):
                shutil.rmtree(self.user_data_dir, ignore_errors=True)
            
            # 创建新的目录
            os.makedirs(self.user_data_dir, exist_ok=True)
            print(f"{Fore.GREEN}✅ 成功清理并创建新的用户数据目录{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ 清理用户数据目录失败: {str(e)}{Style.RESET_ALL}")

    def _get_browser_options(self):
        """获取浏览器配置"""
        co = ChromiumOptions()
        try:
            extension_path = self._get_extension_path()
            co.add_extension(extension_path)

            extension_block_path = self.get_extension_block()
            co.add_extension(extension_block_path)

            extension_recaptcha_path = self.get_extension_recaptcha()
            co.add_extension(extension_recaptcha_path)

        except FileNotFoundError as e:
            logging.warning(f"警告: {e}")

        # 设置用户数据目录
        if self.user_data_dir:
            co.set_argument(f'--user-data-dir={self.user_data_dir}')

        co.set_user_agent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.92 Safari/537.36"
        )
        co.set_pref("credentials_enable_service", False)
        co.set_argument("--hide-crash-restore-bubble")
        co.auto_port()

        # Mac 系统特殊处理
        if sys.platform == "darwin":
            co.set_argument("--no-sandbox")
            co.set_argument("--disable-gpu")

        return co

    def _get_extension_path(self):
        """获取插件路径"""
        root_dir = os.getcwd()
        extension_path = os.path.join(root_dir, "turnstilePatch")

        if hasattr(sys, "_MEIPASS"):
            extension_path = os.path.join(sys._MEIPASS, "turnstilePatch")

        if not os.path.exists(extension_path):
            raise FileNotFoundError(f"插件不存在: {extension_path}")

        return extension_path
    
    def get_extension_block(self):
        """获取插件路径"""
        root_dir = os.getcwd()
        extension_path = os.path.join(root_dir, "uBlock0.chromium")
        
        if hasattr(sys, "_MEIPASS"):
            extension_path = os.path.join(sys._MEIPASS, "uBlock0.chromium")

        if not os.path.exists(extension_path):
            raise FileNotFoundError(f"插件不存在: {extension_path}")

        return extension_path

    def get_extension_recaptcha(self):
        """获取插件路径"""
        root_dir = os.getcwd()
        extension_path = os.path.join(root_dir, "recaptchaPatch")

        if hasattr(sys, "_MEIPASS"):
            extension_path = os.path.join(sys._MEIPASS, "recaptchaPatch")

        if not os.path.exists(extension_path):
            raise FileNotFoundError(f"插件不存在: {extension_path}")

        return extension_path

    def quit(self):
        """关闭浏览器并清理用户数据"""
        if self.browser:
            try:
                self.browser.quit()
            except:
                pass
            finally:
                # 清理用户数据目录
                if self.user_data_dir and os.path.exists(self.user_data_dir):
                    try:
                        shutil.rmtree(self.user_data_dir, ignore_errors=True)
                        print(f"{Fore.GREEN}✅ 成功清理用户数据目录{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}❌ 清理用户数据目录失败: {str(e)}{Style.RESET_ALL}")