import os
from colorama import Fore, Style, init
import time
import random
from browser import BrowserManager
from control import BrowserControl
from cursor_auth import CursorAuth
from reset_machine_manual import MachineIDResetter
from quit_cursor import quit_cursor
import subprocess
import sys

os.environ["PYTHONVERBOSE"] = "0"
os.environ["PYINSTALLER_VERBOSE"] = "0"

# 初始化colorama
init()

# 定义emoji常量
EMOJI = {
    'START': '🚀',
    'FORM': '📝',
    'VERIFY': '🔄',
    'PASSWORD': '🔑',
    'CODE': '📱',
    'DONE': '✨',
    'ERROR': '❌',
    'WAIT': '⏳',
    'SUCCESS': '✅',
    'MAIL': '📧',
    'KEY': '🔐',
    'UPDATE': '🔄',
    'INFO': 'ℹ️',
    'PROCESS': '🔄'
}

class CursorRegistration:
    def __init__(self, translator=None):
        self.translator = translator
        # 设置为显示模式
        os.environ['BROWSER_HEADLESS'] = 'False'
        self.browser_manager = BrowserManager()
        self.browser = None
        self.controller = None
        self.mail_url = "https://yopmail.com/zh/email-generator"
        self.sign_up_url = "https://authenticator.cursor.sh/sign-up"
        self.settings_url = "https://www.cursor.com/settings"
        self.email_address = None
        self.signup_tab = None
        self.email_tab = None
        
        # 账号信息
        self.password = self._generate_password()
        self.first_name = self._generate_name()
        self.last_name = self._generate_name()

    def _generate_password(self, length=12):
        """Generate Random Password"""
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        return ''.join(random.choices(chars, k=length))

    def _generate_name(self, length=6):
        """Generate Random Name"""
        first_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        rest_letters = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=length-1))
        return first_letter + rest_letters

    def setup_email(self):
        """设置邮箱"""
        try:
            print(f"{Fore.CYAN}{EMOJI['START']} {self.translator.get('register.browser_start')}...{Style.RESET_ALL}")
            self.browser = self.browser_manager.init_browser()
            self.controller = BrowserControl(self.browser, self.translator)
            
            # 打开邮箱生成器页面（第一个标签页）
            self.controller.navigate_to(self.mail_url)
            self.email_tab = self.browser  # 保存邮箱标签页
            self.controller.email_tab = self.email_tab  # 同时保存到controller
            
            # 生成新邮箱
            self.controller.generate_new_email()
            
            # 选择随机域名
            self.controller.select_email_domain()
            
            # 获取邮箱地址
            self.email_address = self.controller.copy_and_get_email()
            if self.email_address:
                print(f"{EMOJI['MAIL']}{Fore.CYAN} {self.translator.get('register.get_email_address')}: {self.email_address}{Style.RESET_ALL}")
                
                # 进入邮箱
                if self.controller.view_mailbox():
                    return True
            
            return False
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.setup_error', error=str(e))}{Style.RESET_ALL}")
            return False

    def register_cursor(self):
        """注册 Cursor"""
        signup_browser_manager = None
        try:
            print(f"{Fore.CYAN}{EMOJI['START']} {self.translator.get('register.register_start')}...{Style.RESET_ALL}")
            
            # 创建新的浏览器实例用于注册
            from browser import BrowserManager
            signup_browser_manager = BrowserManager(noheader=True)
            self.signup_tab = signup_browser_manager.init_browser()
            
            # 访问注册页面
            self.signup_tab.get(self.sign_up_url)
            time.sleep(2)

            # 填写注册表单
            if self.signup_tab.ele("@name=first_name"):
                print(f"{Fore.CYAN}{EMOJI['FORM']} {self.translator.get('register.filling_form')}...{Style.RESET_ALL}")
                
                self.signup_tab.ele("@name=first_name").input(self.first_name)
                time.sleep(random.uniform(1, 2))
                
                self.signup_tab.ele("@name=last_name").input(self.last_name)
                time.sleep(random.uniform(1, 2))
                
                self.signup_tab.ele("@name=email").input(self.email_address)
                time.sleep(random.uniform(1, 2))
                
                self.signup_tab.ele("@type=submit").click()
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.basic_info_submitted')}...{Style.RESET_ALL}")

                # 等待页面加载完成
                time.sleep(3)

                # 检查人机验证状态
                max_verify_attempts = 3
                verify_attempt = 0
                
                while verify_attempt < max_verify_attempts:
                    # 处理 Turnstile 验证
                    verify_result = self._handle_turnstile()
                    
                    if verify_result:
                        break
                    
                    # 如果验证失败，重新填写表单
                    print(f"{Fore.CYAN}{EMOJI['FORM']} {self.translator.get('register.refilling_basic_info')}...{Style.RESET_ALL}")
                    
                    # 等待页面刷新完成
                    time.sleep(3)
                    
                    # 重新填写表单
                    try:
                        first_name_input = self.signup_tab.ele("@name=first_name")
                        if first_name_input:
                            first_name_input.input(self.first_name)
                            time.sleep(random.uniform(1, 2))
                        
                        last_name_input = self.signup_tab.ele("@name=last_name")
                        if last_name_input:
                            last_name_input.input(self.last_name)
                            time.sleep(random.uniform(1, 2))
                        
                        email_input = self.signup_tab.ele("@name=email")
                        if email_input:
                            email_input.input(self.email_address)
                            time.sleep(random.uniform(1, 2))
                        
                        submit_button = self.signup_tab.ele("@type=submit")
                        if submit_button:
                            submit_button.click()
                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.form_resubmitted')}...{Style.RESET_ALL}")
                            
                            # 等待页面加载和可能的验证出现
                            time.sleep(5)
                    except Exception as e:
                        print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('register.human_behavior_error', error=str(e))}")
                    
                    verify_attempt += 1
                    
                    if verify_attempt >= max_verify_attempts:
                        print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.max_verify_attempts')}...{Style.RESET_ALL}")
                        return False

            # 设置密码
            if self.signup_tab.ele("@name=password"):
                print(f"{Fore.CYAN}{EMOJI['PASSWORD']} {self.translator.get('register.set_password')}...{Style.RESET_ALL}")
                self.signup_tab.ele("@name=password").input(self.password)
                time.sleep(random.uniform(1, 2))
                self.signup_tab.ele("@type=submit").click()
                
                # 等待页面加载完成
                time.sleep(3)
                
                # 检查密码页面的人机验证
                max_verify_attempts = 3
                verify_attempt = 0
                
                while verify_attempt < max_verify_attempts:
                    # 处理 Turnstile 验证
                    verify_result = self._handle_turnstile()
                    
                    if verify_result:
                        break
                    
                    # 如果验证失败，重新填写密码
                    print(f"{Fore.CYAN}{EMOJI['PASSWORD']} {self.translator.get('register.refilling_password')}...{Style.RESET_ALL}")
                    
                    # 等待页面刷新完成
                    time.sleep(3)
                    
                    # 重新填写密码
                    try:
                        password_input = self.signup_tab.ele("@name=password")
                        if password_input:
                            password_input.input(self.password)
                            time.sleep(random.uniform(1, 2))
                        
                        submit_button = self.signup_tab.ele("@type=submit")
                        if submit_button:
                            submit_button.click()
                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.password_resubmitted')}...{Style.RESET_ALL}")
                            
                            # 等待页面加载和可能的验证出现
                            time.sleep(5)
                    except Exception as e:
                        print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('register.human_behavior_error', error=str(e))}")
                    
                    verify_attempt += 1
                    
                    if verify_attempt >= max_verify_attempts:
                        print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.max_verify_attempts')}...{Style.RESET_ALL}")
                        return False

            # 等待并获取验证码
            time.sleep(5)  # 等待验证码邮件

            self.browser.refresh()
            
            # 获取验证码，设置60秒超时
            verification_code = None
            max_attempts = 10  # 增加到10次尝试
            retry_interval = 5  # 每5秒重试一次
            start_time = time.time()
            timeout = 60  # 60秒超时

            print(f"{Fore.CYAN}{EMOJI['WAIT']} {self.translator.get('register.start_getting_verification_code')}...{Style.RESET_ALL}")
            
            for attempt in range(max_attempts):
                # 检查是否超时
                if time.time() - start_time > timeout:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.get_verification_code_timeout')}...{Style.RESET_ALL}")
                    break
                    
                verification_code = self.controller.get_verification_code()
                if verification_code:
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.get_verification_code_success')}: {verification_code}{Style.RESET_ALL}")
                    break
                    
                remaining_time = int(timeout - (time.time() - start_time))
                print(f"{Fore.YELLOW}{EMOJI['WAIT']} {self.translator.get('register.try_get_verification_code', attempt=attempt + 1, remaining_time=remaining_time)}...{Style.RESET_ALL}")
                
                # 刷新邮箱
                self.browser.refresh()
                time.sleep(retry_interval)
            
            if verification_code:
                # 在注册页面填写验证码
                for i, digit in enumerate(verification_code):
                    self.signup_tab.ele(f"@data-index={i}").input(digit)
                    time.sleep(random.uniform(0.1, 0.3))
                
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.verification_code_filled')}...{Style.RESET_ALL}")
                time.sleep(3)

                self._handle_turnstile()
                
                # 检查当前URL
                current_url = self.signup_tab.url
                if "authenticator.cursor.sh" in current_url:
                    print(f"{Fore.CYAN}{EMOJI['VERIFY']} {self.translator.get('register.detect_login_page')}...{Style.RESET_ALL}")
                    
                    # 填写邮箱
                    email_input = self.signup_tab.ele('@name=email')
                    if email_input:
                        email_input.input(self.email_address)
                        time.sleep(random.uniform(1, 2))
                        
                        # 点击提交
                        submit_button = self.signup_tab.ele('@type=submit')
                        if submit_button:
                            submit_button.click()
                            time.sleep(2)
                            
                            # 处理 Turnstile 验证
                            self._handle_turnstile()
                            
                            # 填写密码
                            password_input = self.signup_tab.ele('@name=password')
                            if password_input:
                                password_input.input(self.password)
                                time.sleep(random.uniform(1, 2))
                                
                                # 点击提交
                                submit_button = self.signup_tab.ele('@type=submit')
                                if submit_button:
                                    submit_button.click()
                                    time.sleep(2)
                                    
                                    # 处理 Turnstile 验证
                                    self._handle_turnstile()
                                    
                                    # 等待跳转到设置页面
                                    max_wait = 30
                                    start_time = time.time()
                                    while time.time() - start_time < max_wait:
                                        if "cursor.com/settings" in self.signup_tab.url:
                                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.login_success_and_jump_to_settings_page')}...{Style.RESET_ALL}")
                                            break
                                        time.sleep(1)
                
                # 获取账户信息
                result = self._get_account_info()
                
                # 关闭注册窗口
                if signup_browser_manager:
                    signup_browser_manager.quit()
                    
                return result
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.get_verification_code_timeout')}...{Style.RESET_ALL}")
                return False

        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.register_process_error', error=str(e))}{Style.RESET_ALL}")
            return False
        finally:
            # 确保在任何情况下都关闭注册窗口
            if signup_browser_manager:
                signup_browser_manager.quit()

    def _handle_turnstile(self):
        """处理 Turnstile 验证"""
        try:
            print(f"{Fore.CYAN}{EMOJI['VERIFY']} {self.translator.get('register.handling_turnstile')}...{Style.RESET_ALL}")
            
            # 等待页面加载完成
            time.sleep(3)
            
            # 检查是否存在人机验证错误
            error_messages = [
                "Can't verify the user is human",
                "Please try again",
                "人机验证失败",
                "请重试"
            ]
            
            # 检查页面文本中是否包含错误信息
            page_text = self.signup_tab.text
            for error_msg in error_messages:
                if error_msg in page_text:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.human_verify_failed')}: {error_msg}")
                    return False
            
            # 检查是否存在验证框架
            iframe = self.signup_tab.ele("iframe[title*='Turnstile']")
            if not iframe:
                print(f"{Fore.YELLOW}{EMOJI['WAIT']} {self.translator.get('register.no_turnstile_detected')}...{Style.RESET_ALL}")
                return True
                
            # 等待验证完成
            max_wait = 30
            start_time = time.time()
            while time.time() - start_time < max_wait:
                # 再次检查错误信息
                page_text = self.signup_tab.text
                for error_msg in error_messages:
                    if error_msg in page_text:
                        print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.human_verify_failed')}: {error_msg}")
                        return False
                
                # 检查是否还存在验证框架
                if not self.signup_tab.ele("iframe[title*='Turnstile']"):
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.turnstile_verified')}...{Style.RESET_ALL}")
                    return True
                    
                time.sleep(0.5)  # 每500ms检查一次
                
            print(f"{Fore.YELLOW}{EMOJI['WAIT']} {self.translator.get('register.turnstile_timeout')}...{Style.RESET_ALL}")
            return False
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.turnstile_error', error=str(e))}...{Style.RESET_ALL}")
            return False

    def _check_human_verify(self):
        """检查是否出现人机验证失败提示"""
        try:
            error_texts = [
                "Can't verify the user is human",
                "Please try again",
                "人机验证失败",
                "请重试"
            ]
            
            for text in error_texts:
                error_element = self.signup_tab.ele(f'xpath://div[contains(text(), "{text}")]')
                if error_element:
                    return True
            return False
        except:
            return False

    def _refill_form(self):
        """重新填写表单"""
        try:
            print(f"{Fore.CYAN}{EMOJI['FORM']} {self.translator.get('register.refilling_basic_info')}...{Style.RESET_ALL}")
            
            # 等待页面加载完成
            time.sleep(2)
            
            # 检查并等待元素可见
            def wait_for_element(selector, timeout=10):
                start_time = time.time()
                while time.time() - start_time < timeout:
                    element = self.signup_tab.ele(selector)
                    if element and element.is_displayed():
                        # 确保元素完全加载并可交互
                        time.sleep(0.5)
                        return element
                    time.sleep(0.5)
                return None
            
            # 填写表单
            first_name_input = wait_for_element("@name=first_name")
            if not first_name_input:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.element_not_found', field='first_name')}...{Style.RESET_ALL}")
                return False
                
            # 清空输入框
            first_name_input.clear()
            time.sleep(random.uniform(0.5, 1))
            
            # 模拟人类输入
            for char in self.first_name:
                first_name_input.input(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            # 等待一下再输入下一个字段
            time.sleep(random.uniform(0.5, 1))
            
            # 重复类似步骤填写 last_name 和 email
            last_name_input = wait_for_element("@name=last_name")
            if not last_name_input:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.element_not_found', field='last_name')}...{Style.RESET_ALL}")
                return False
                
            last_name_input.clear()
            time.sleep(random.uniform(0.5, 1))
            
            for char in self.last_name:
                last_name_input.input(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            time.sleep(random.uniform(0.5, 1))
            
            email_input = wait_for_element("@name=email")
            if not email_input:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.element_not_found', field='email')}...{Style.RESET_ALL}")
                return False
                
            email_input.clear()
            time.sleep(random.uniform(0.5, 1))
            
            for char in self.email_address:
                email_input.input(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            # 等待一下再点击提交按钮
            time.sleep(random.uniform(1, 2))
            
            # 查找并点击提交按钮
            submit_button = wait_for_element("@type=submit")
            if not submit_button:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.submit_button_not_found')}...{Style.RESET_ALL}")
                return False
                
            submit_button.click()
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.form_resubmitted')}...{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.refill_form_error', error=str(e))}...{Style.RESET_ALL}")
            return False

    def _simulate_human_behavior(self):
        """模拟人类行为"""
        try:
            # 随机鼠标移动
            elements = self.signup_tab.eles('xpath://*')
            for _ in range(random.randint(2, 4)):
                random_element = random.choice(elements)
                self.signup_tab.actions.move_to(random_element)
                time.sleep(random.uniform(0.3, 0.8))
            
            # 随机滚动
            scroll_amounts = [100, 200, -100, -150]
            for _ in range(random.randint(1, 3)):
                scroll_amount = random.choice(scroll_amounts)
                self.signup_tab.execute_script(f"window.scrollBy(0, {scroll_amount})")
                time.sleep(random.uniform(0.5, 1))
            
            # 模拟页面浏览暂停
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"{Fore.YELLOW}{EMOJI['INFO']} 模拟人类行为时出错: {str(e)}{Style.RESET_ALL}")

    def _get_account_info(self):
        """获取账户信息"""
        try:
            time.sleep(3)
            token = None
            usage_limit = None
            current_url = self.signup_tab.url
            if "token=" in current_url:
                token = current_url.split("token=")[1].split("&")[0]
            
            print(f"{Fore.CYAN}{EMOJI['KEY']} {self.translator.get('register.update_cursor_auth_info')}...{Style.RESET_ALL}")
            if self.update_cursor_auth(email=self.email_address, access_token=token, refresh_token=token):
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.cursor_auth_info_updated')}...{Style.RESET_ALL}")
                
                # 保存账号信息到文件
                self.save_account_info(self.email_address, self.password, token, usage_limit)
                
                # 提示用户正在切换到新账号
                print(f"\n{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('register.switching_account')}...{Style.RESET_ALL}")
                
                # 退出当前 Cursor IDE
                print(f"{Fore.YELLOW}{EMOJI['PROCESS']} {self.translator.get('register.quitting_cursor')}...{Style.RESET_ALL}")
                quit_cursor(self.translator)
                
                # 等待几秒确保完全退出
                time.sleep(3)
                
                # 重启 Cursor IDE
                print(f"{Fore.CYAN}{EMOJI['START']} {self.translator.get('register.restarting_cursor')}...{Style.RESET_ALL}")
                self._restart_cursor()
                
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.account_switch_complete')}...{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.cursor_auth_info_update_failed')}...{Style.RESET_ALL}")
                return False
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.get_account_info_error', error=str(e))}{Style.RESET_ALL}")
            return False

    def _check_network(self):
        """检查网络连接状态"""
        try:
            import socket
            # 尝试连接到 Cursor 服务器
            socket.create_connection(("cursor.sh", 443), timeout=5)
            return True
        except:
            return False

    def _restart_cursor(self):
        """重启 Cursor IDE"""
        try:
            print(f"{Fore.CYAN}{EMOJI['START']} {self.translator.get('register.restarting_cursor')}...{Style.RESET_ALL}")
            
            # 等待旧进程完全退出
            time.sleep(3)
            
            # 检查网络连接
            if not self._check_network():
                print(f"{Fore.YELLOW}{EMOJI['WAIT']} 网络连接不稳定，等待重试...{Style.RESET_ALL}")
                time.sleep(2)
                if not self._check_network():
                    print(f"{Fore.YELLOW}{EMOJI['WAIT']} 继续等待网络恢复...{Style.RESET_ALL}")
                    time.sleep(5)
                    if not self._check_network():
                        print(f"{Fore.RED}{EMOJI['ERROR']} 网络连接不稳定，请检查网络后重试{Style.RESET_ALL}")
                        return False
            
            # 启动新进程
            if sys.platform == "win32":
                cursor_path = os.path.join(os.getenv("LOCALAPPDATA"), "Programs", "Cursor", "Cursor.exe")
                if os.path.exists(cursor_path):
                    subprocess.Popen([cursor_path])
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Cursor IDE 启动成功{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}{EMOJI['ERROR']} 未找到 Cursor IDE 程序{Style.RESET_ALL}")
                    return False
            elif sys.platform == "darwin":  # macOS
                try:
                    subprocess.Popen(["open", "-a", "Cursor"])
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Cursor IDE 启动成功{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}{EMOJI['ERROR']} 启动 Cursor IDE 失败: {str(e)}{Style.RESET_ALL}")
                    return False
            
            # 等待启动完成
            time.sleep(5)
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.restart_cursor_error', error=str(e))}{Style.RESET_ALL}")
            return False

    def save_account_info(self, email, password, token=None, usage_limit=None):
        """保存账号信息到文件"""
        try:
            account_info = {
                "email": email,
                "password": password,
                "token": token,
                "usage_limit": usage_limit,
                "registration_time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 确保文件存在
            filename = "cursor_accounts.txt"
            if not os.path.exists(filename):
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("")
            
            # 读取现有账号
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 添加分隔线和新账号信息
            with open(filename, "a", encoding="utf-8") as f:
                if content and not content.endswith("\n"):
                    f.write("\n")
                if content:
                    f.write("\n" + "="*50 + "\n")
                f.write(f"Registration Time: {account_info['registration_time']}\n")
                f.write(f"Email: {account_info['email']}\n")
                f.write(f"Password: {account_info['password']}\n")
                if token:
                    f.write(f"Token: {account_info['token']}\n")
                if usage_limit:
                    f.write(f"Usage Limit: {account_info['usage_limit']}\n")
            
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('register.account_info_saved')}...{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('register.save_account_info_error', error=str(e))}{Style.RESET_ALL}")

    def start(self):
        """启动注册流程"""
        try:
            if self.setup_email():
                if self.register_cursor():
                    print(f"\n{Fore.GREEN}{EMOJI['DONE']} {self.translator.get('register.cursor_registration_completed')}...{Style.RESET_ALL}")
                    return True
            return False
        finally:
            if self.browser_manager:
                self.browser_manager.quit()

    def update_cursor_auth(self, email=None, access_token=None, refresh_token=None):
        """更新Cursor的认证信息的便捷函数"""
        auth_manager = CursorAuth(translator=self.translator)
        return auth_manager.update_auth(email, access_token, refresh_token)

def main(translator=None):
    """Main function to be called from main.py"""
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['START']} {translator.get('register.title')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")

    registration = CursorRegistration(translator)
    registration.start()

    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    input(f"{EMOJI['INFO']} {translator.get('register.press_enter')}...")

if __name__ == "__main__":
    from main import translator as main_translator
    main(main_translator) 