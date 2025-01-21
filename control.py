import time
import random
import os
from colorama import Fore, Style, init

# 初始化colorama
init()

# 定义emoji常量
EMOJI = {
    'MAIL': '📧',
    'REFRESH': '🔄',
    'SUCCESS': '✅',
    'ERROR': '❌',
    'INFO': 'ℹ️',
    'CODE': '📱',
    'VERIFY': '🔍',
    'WAIT': '⏳'
}

class BrowserControl:
    def __init__(self, browser, translator=None):
        self.browser = browser
        self.translator = translator  # 保存translator
        self.sign_up_url = "https://authenticator.cursor.sh/sign-up"
        self.current_tab = None  # 当前标签页
        self.signup_tab = None   # 注册标签页
        self.email_tab = None    # 邮箱标签页
        self.max_verify_retries = 3  # 最大重试次数
        self.verify_wait_time = 2  # 每次检查间隔时间（秒）

    def create_new_tab(self):
        """创建新标签页"""
        try:
            # 保存当前标签页
            self.current_tab = self.browser
            
            # 创建新的浏览器实例
            from browser import BrowserManager
            browser_manager = BrowserManager()
            new_browser = browser_manager.init_browser()
            
            # 保存新标签页
            self.signup_tab = new_browser
            
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('control.create_new_tab_success')}{Style.RESET_ALL}")
            return new_browser
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.create_new_tab_failed', error=str(e))}{Style.RESET_ALL}")
            return None

    def switch_to_tab(self, browser):
        """切换到指定浏览器窗口"""
        try:
            self.browser = browser
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('control.switch_tab_success')}{Style.RESET_ALL}")
            return True
        except Exception as e:  
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.switch_tab_failed', error=str(e))}{Style.RESET_ALL}")
            return False

    def get_current_tab(self):
        """获取当前标签页"""
        return self.browser

    def generate_new_email(self):
        """点击新的按钮生成新邮箱"""
        try:
            print(f"{Fore.CYAN}{EMOJI['MAIL']} {self.translator.get('control.generate_email')}...{Style.RESET_ALL}")
            new_button = self.browser.ele('xpath://button[contains(@class, "egenbut")]')
            if new_button:
                new_button.click()
                time.sleep(1)  # 等待生成
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('control.generate_email_success')}{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.generate_email_failed')}{Style.RESET_ALL}")
                return False
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.browser_error', error=str(e))}{Style.RESET_ALL}")
            return False

    def select_email_domain(self, domain_index=None):
        """选择邮箱域名，如果不指定index则随机选择"""
        try:
            print(f"{Fore.CYAN}{EMOJI['MAIL']} {self.translator.get('control.select_email_domain')}...{Style.RESET_ALL}")
            # 找到下拉框
            select_element = self.browser.ele('xpath://select[@id="seldom"]')
            if select_element:
                # 获取所有选项，包括两个 optgroup 下的所有 option
                all_options = []
                
                # 获取 "新的" 组下的选项
                new_options = self.browser.eles('xpath://select[@id="seldom"]/optgroup[@label="-- 新的 --"]/option')
                all_options.extend(new_options)
                
                # 获取 "其他" 组下的选项
                other_options = self.browser.eles('xpath://select[@id="seldom"]/optgroup[@label="-- 其他 --"]/option')
                all_options.extend(other_options)
                
                if all_options:
                    # 如果没有指定索引，随机选择一个
                    if domain_index is None:
                        domain_index = random.randint(0, len(all_options) - 1)
                    
                    if domain_index < len(all_options):
                        # 获取选中选项的文本
                        selected_domain = all_options[domain_index].text
                        print(f"{Fore.CYAN}{EMOJI['MAIL']} {self.translator.get('control.select_email_domain')}: {selected_domain}{Style.RESET_ALL}")
                        
                        # 点击选择
                        all_options[domain_index].click()
                        time.sleep(1)
                        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('control.select_email_domain_success')}{Style.RESET_ALL}")
                        return True
                    
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.no_available_domain_options', count=len(all_options))}{Style.RESET_ALL}")
                return False
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.no_domain_select_box')}{Style.RESET_ALL}")
                return False
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.select_email_domain_failed', error=str(e))}{Style.RESET_ALL}")
            return False

    def wait_for_page_load(self, seconds=2):
        """等待页面加载"""
        time.sleep(seconds)

    def navigate_to(self, url):
        """导航到指定URL"""
        try:
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('control.navigate_to', url=url)}...{Style.RESET_ALL}")
            self.browser.get(url)
            self.wait_for_page_load()
            return True
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.browser_error', error=str(e))}{Style.RESET_ALL}")
            return False

    def copy_and_get_email(self):
        """获取邮箱地址"""
        try:
            print(f"{Fore.CYAN}{EMOJI['MAIL']} {self.translator.get('control.generate_email')}...{Style.RESET_ALL}")
            
            # 等待元素加载
            time.sleep(1)
            
            # 获取邮箱名称
            try:
                email_div = self.browser.ele('xpath://div[@class="segen"]//div[contains(@style, "color: #e5e5e5")]')
                if email_div:
                    email_name = email_div.text.split()[0]
                    print(f"{Fore.CYAN}{EMOJI['MAIL']} {self.translator.get('control.get_email_name')}: {email_name}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.get_email_name_failed')}{Style.RESET_ALL}")
                    return None
            except Exception as e:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.get_email_name_failed', error=str(e))}{Style.RESET_ALL}")
                return None
            
            # 直接使用上一步选择的域名
            try:
                domain = self.browser.ele('xpath://select[@id="seldom"]').value
                if not domain:  # 如果获取不到value，尝试获取选中的选项文本
                    selected_option = self.browser.ele('xpath://select[@id="seldom"]/option[1]')
                    domain = selected_option.text if selected_option else "@yopmail.com"  # 使用默认域名作为后备
            except:
                domain = "@yopmail.com"  # 如果出错，使用默认域名
            
            # 组合完整邮箱地址
            full_email = f"{email_name}{domain}"
            print(f"{Fore.GREEN}{EMOJI['MAIL']} {self.translator.get('control.get_email_address')}: {full_email}{Style.RESET_ALL}")
            return full_email
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.get_email_address_failed', error=str(e))}{Style.RESET_ALL}")
            return None 

    def view_mailbox(self):
        """点击查看邮箱按钮"""
        try:
            print(f"{Fore.CYAN}{EMOJI['MAIL']} {self.translator.get('control.enter_mailbox')}...{Style.RESET_ALL}")
            view_button = self.browser.ele('xpath://button[contains(@class, "egenbut") and contains(.//span, "查看邮箱")]')
            if view_button:
                view_button.click()
                time.sleep(2)  # 等待页面加载
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('control.enter_mailbox_success')}{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.no_view_mailbox_button')}{Style.RESET_ALL}")
                return False
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.enter_mailbox_failed', error=str(e))}{Style.RESET_ALL}")
            return False 

    def refresh_mailbox(self):
        """刷新邮箱获取最新信息"""
        try:
            print(f"{Fore.CYAN}{EMOJI['MAIL']} {self.translator.get('control.refresh_mailbox')}...{Style.RESET_ALL}")
            refresh_button = self.browser.ele('xpath://button[@id="refresh"]')
            if refresh_button:
                refresh_button.click()
                time.sleep(2)  # 等待刷新完成
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('control.refresh_mailbox_success')}{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.no_refresh_button')}{Style.RESET_ALL}")
                return False
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.refresh_mailbox_failed', error=str(e))}{Style.RESET_ALL}")
            return False 


    def get_verification_code(self):
        """从邮件中获取验证码"""
        try:
            print(f"\n{Fore.YELLOW}{EMOJI['INFO']} ================================================{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{EMOJI['INFO']} 请按照以下步骤手动操作：{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{EMOJI['INFO']} 1. 在邮箱页面中查看最新的验证码邮件{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{EMOJI['INFO']} 2. 如果没有收到邮件，请点击刷新按钮{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{EMOJI['INFO']} 3. 等待邮件出现并显示验证码{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{EMOJI['INFO']} 4. 程序会自动识别验证码{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{EMOJI['INFO']} ================================================\n{Style.RESET_ALL}")
            
            # 等待用户查看提示
            time.sleep(3)
            
            # 尝试所有可能的样式组合
            selectors = [
                # 新样式
                'xpath://div[contains(@style, "font-family:-apple-system") and contains(@style, "font-size:28px") and contains(@style, "letter-spacing:2px") and contains(@style, "color:#202020")]',
                # 带行高的样式
                'xpath://div[contains(@style, "font-size:28px") and contains(@style, "letter-spacing:2px") and contains(@style, "line-height:30px")]',
                # rgba 颜色样式
                'xpath://div[contains(@style, "font-size: 28px") and contains(@style, "letter-spacing: 2px") and contains(@style, "color: rgba(32, 32, 32, 1)")]',
                # 宽松样式
                'xpath://div[contains(@style, "font-size:28px") and contains(@style, "letter-spacing:2px")]'
            ]
            
            max_attempts = 30  # 最多等待60秒
            attempt = 0
            
            while attempt < max_attempts:
                # 依次尝试每个选择器
                for selector in selectors:
                    code_div = self.browser.ele(selector)
                    if code_div:
                        verification_code = code_div.text.strip()
                        if verification_code.isdigit() and len(verification_code) == 6:
                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} 成功获取验证码: {verification_code}{Style.RESET_ALL}")
                            return verification_code
                
                # 如果没有找到验证码
                if attempt % 5 == 0:  # 每5次检查显示一次提示
                    print(f"{Fore.CYAN}{EMOJI['WAIT']} 正在等待验证码出现... ({attempt}/{max_attempts}){Style.RESET_ALL}")
                
                attempt += 1
                time.sleep(2)  # 每2秒检查一次
            
            print(f"\n{Fore.RED}{EMOJI['ERROR']} ================================================{Style.RESET_ALL}")
            print(f"{Fore.RED}{EMOJI['ERROR']} 未能自动获取到验证码，请检查：{Style.RESET_ALL}")
            print(f"{Fore.RED}{EMOJI['ERROR']} 1. 邮件是否已送达{Style.RESET_ALL}")
            print(f"{Fore.RED}{EMOJI['ERROR']} 2. 是否需要手动刷新邮箱{Style.RESET_ALL}")
            print(f"{Fore.RED}{EMOJI['ERROR']} 3. 验证码邮件是否被过滤{Style.RESET_ALL}")
            print(f"{Fore.RED}{EMOJI['ERROR']} ================================================\n{Style.RESET_ALL}")
            return None
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} 获取验证码时出错: {str(e)}{Style.RESET_ALL}")
            return None

    def save_account_info(self, email, password, token=None, usage_limit=None):
        """保存账号信息"""
        try:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            with open('cursor_accounts.txt', 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"注册时间: {current_time}\n")
                f.write(f"邮箱账号: {email}\n")
                f.write(f"账号密码: {password}\n")
                if token:
                    f.write(f"账号Token: {token}\n")
                if usage_limit:
                    f.write(f"使用额度: {usage_limit}\n")
                f.write(f"{'='*50}\n")
            
            # 在控制台显示账号信息
            print(f"\n{Fore.GREEN}{EMOJI['SUCCESS']} ================================================{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} 注册成功！账号信息如下：{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{EMOJI['INFO']} 邮箱账号: {email}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{EMOJI['INFO']} 账号密码: {password}{Style.RESET_ALL}")
            if usage_limit:
                print(f"{Fore.GREEN}{EMOJI['INFO']} 使用额度: {usage_limit}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{EMOJI['INFO']} 账号信息已保存至 cursor_accounts.txt{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} ================================================\n{Style.RESET_ALL}")
            
            return True
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} 保存账号信息失败: {str(e)}{Style.RESET_ALL}")
            return False

    def fill_verification_code(self, code):
        """填写验证码"""
        try:
            # 先检查注册页面状态
            if self.check_human_verify():
                print(f"{Fore.RED}{EMOJI['ERROR']} 检测到人机验证失败，需要重新验证{Style.RESET_ALL}")
                return False

            # 检查是否存在验证码输入框
            verification_input = self.browser.ele('xpath://input[@type="text" and @inputmode="numeric"]')
            if not verification_input:
                print(f"{Fore.RED}{EMOJI['ERROR']} 未检测到验证码输入框，可能验证失败{Style.RESET_ALL}")
                return False

            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('control.fill_verification_code')}...{Style.RESET_ALL}")
            
            # 记住当前标签页（注册页面）
            signup_tab = self.browser
            
            # 切换到邮箱页面
            self.switch_to_tab(self.email_tab)
            time.sleep(1)
            
            # 获取验证码
            verification_code = self.get_verification_code()
            if not verification_code:
                print(f"{Fore.RED}{EMOJI['ERROR']} 未能获取到验证码{Style.RESET_ALL}")
                return False
            
            # 切换回注册页面
            self.switch_to_tab(signup_tab)
            time.sleep(1)
            
            # 再次检查页面状态
            if self.check_human_verify():
                print(f"{Fore.RED}{EMOJI['ERROR']} 检测到人机验证失败，需要重新验证{Style.RESET_ALL}")
                return False
            
            # 确认验证码输入框仍然存在
            verification_input = self.browser.ele('xpath://input[@type="text" and @inputmode="numeric"]')
            if not verification_input:
                print(f"{Fore.RED}{EMOJI['ERROR']} 验证码输入框已消失，可能需要重新验证{Style.RESET_ALL}")
                return False
            
            # 输入验证码
            for digit in verification_code:
                verification_input.send_keys(digit)
                time.sleep(random.uniform(0.1, 0.3))
            
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('control.verification_code_filled')}{Style.RESET_ALL}")
            
            # 等待页面加载和登录完成
            print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('control.wait_for_login')}...{Style.RESET_ALL}")
            time.sleep(5)
            
            # 再次检查页面状态
            if self.check_human_verify():
                print(f"{Fore.RED}{EMOJI['ERROR']} 验证码提交后检测到人机验证失败{Style.RESET_ALL}")
                return False
            
            # 获取token和账户信息
            token = self.get_cursor_session_token()
            usage_limit = None
            
            if token:
                self.save_token_to_file(token)
                
                # 获取到token后再访问设置页面
                settings_url = "https://www.cursor.com/settings"
                print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('control.get_account_info')}...{Style.RESET_ALL}")
                self.browser.get(settings_url)
                time.sleep(2)
                
                # 获取账户额度信息
                try:
                    usage_selector = (
                        "css:div.col-span-2 > div > div > div > div > "
                        "div:nth-child(1) > div.flex.items-center.justify-between.gap-2 > "
                        "span.font-mono.text-sm\\/\\[0\\.875rem\\]"
                    )
                    usage_ele = self.browser.ele(usage_selector)
                    if usage_ele:
                        usage_info = usage_ele.text
                        usage_limit = usage_info.split("/")[-1].strip()
                        print(f"{Fore.GREEN}{EMOJI['INFO']} {self.translator.get('control.account_usage_limit')}: {usage_limit}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.get_account_usage_failed', error=str(e))}{Style.RESET_ALL}")
            
            # 保存账号信息
            self.save_account_info(self.email_address, self.password, token, usage_limit)
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.fill_verification_code_failed', error=str(e))}{Style.RESET_ALL}")
            return False

    def check_and_click_turnstile(self):
        """检查并点击 Turnstile 验证框，并验证结果"""
        try:
            # 等待验证框出现
            time.sleep(1)
            
            # 查找验证框
            verify_checkbox = self.browser.ele('xpath://label[contains(@class, "cb-lb")]//input[@type="checkbox"]')
            if verify_checkbox:
                print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('control.find_turnstile_verification_box')}...{Style.RESET_ALL}")
                verify_checkbox.click()
                
                # 等待验证完成
                for _ in range(10):  # 最多等待10次
                    time.sleep(2)  # 每次等待2秒
                    
                    # 检查是否出现人机验证失败
                    if self.check_human_verify():
                        print(f"{Fore.RED}{EMOJI['ERROR']} Turnstile验证失败{Style.RESET_ALL}")
                        return False
                    
                    # 检查是否验证成功（验证框消失或变为已验证状态）
                    try:
                        new_checkbox = self.browser.ele('xpath://label[contains(@class, "cb-lb")]//input[@type="checkbox"]')
                        if not new_checkbox or new_checkbox.get_attribute('checked'):
                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Turnstile验证成功{Style.RESET_ALL}")
                            
                            # 再次确认没有人机验证失败提示
                            time.sleep(2)
                            if not self.check_human_verify():
                                return True
                    except:
                        pass
                
                print(f"{Fore.RED}{EMOJI['ERROR']} Turnstile验证超时{Style.RESET_ALL}")
                return False
            
            print(f"{Fore.YELLOW}{EMOJI['INFO']} 未检测到 Turnstile 验证框{Style.RESET_ALL}")
            return False
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Turnstile验证出错: {str(e)}{Style.RESET_ALL}")
            return False

    def wait_for_verification_result(self, timeout=30):
        """等待验证结果，持续检查人机验证状态"""
        print(f"{Fore.CYAN}{EMOJI['INFO']} 等待验证结果...{Style.RESET_ALL}")
        start_time = time.time()
        check_interval = 2  # 每2秒检查一次
        
        while time.time() - start_time < timeout:
            if self.check_human_verify():
                print(f"{Fore.RED}{EMOJI['ERROR']} 检测到人机验证失败{Style.RESET_ALL}")
                return False
                
            # 检查是否存在验证码输入框（成功标志）
            verification_input = self.browser.ele('xpath://input[@type="text" and @inputmode="numeric"]')
            if verification_input:
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} 验证成功{Style.RESET_ALL}")
                return True
                
            time.sleep(check_interval)
            
        print(f"{Fore.RED}{EMOJI['ERROR']} 验证等待超时{Style.RESET_ALL}")
        return False

    def get_cursor_session_token(self, max_attempts=3, retry_interval=2):
        """获取Cursor会话token"""
        print(f"{Fore.CYAN}{EMOJI['INFO']} {self.translator.get('control.get_cursor_session_token')}...{Style.RESET_ALL}")
        attempts = 0

        while attempts < max_attempts:
            try:
                # 直接从浏览器对象获取cookies
                all_cookies = self.browser.get_cookies()
                
                # 遍历查找目标cookie
                for cookie in all_cookies:
                    if cookie.get("name") == "WorkosCursorSessionToken":
                        token = cookie["value"].split("%3A%3A")[1]
                        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('control.get_cursor_session_token_success')}: {token}{Style.RESET_ALL}")
                        return token

                attempts += 1
                if attempts < max_attempts:
                    print(f"{Fore.YELLOW}{EMOJI['ERROR']} {self.translator.get('control.get_cursor_session_token_failed', attempts=attempts, retry_interval=retry_interval)}...{Style.RESET_ALL}")
                    time.sleep(retry_interval)
                else:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.reach_max_attempts', max_attempts=max_attempts)}{Style.RESET_ALL}")

            except Exception as e:
                print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.get_cookie_failed', error=str(e))}{Style.RESET_ALL}")
                attempts += 1
                if attempts < max_attempts:
                    print(f"{Fore.YELLOW}{EMOJI['ERROR']} {self.translator.get('control.will_retry_in', retry_interval=retry_interval)}...{Style.RESET_ALL}")
                    time.sleep(retry_interval)

        return None

    def save_token_to_file(self, token):
        """保存token到文件"""
        try:
            with open('cursor_tokens.txt', 'a', encoding='utf-8') as f:
                f.write(f"Token: {token}\n")
                f.write("-" * 50 + "\n")
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {self.translator.get('control.token_saved_to_file')}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {self.translator.get('control.save_token_failed', error=str(e))}{Style.RESET_ALL}") 

    def check_human_verify(self):
        """检查是否出现人机验证失败的提示"""
        try:
            print(f"{Fore.CYAN}{EMOJI['VERIFY']} 检查人机验证状态...{Style.RESET_ALL}")
            # 等待一段时间让页面加载
            time.sleep(self.verify_wait_time)
            
            # 查找所有可能的错误提示文本
            error_texts = [
                "Can't verify the user is human",
                "Please try again",
                "人机验证失败",
                "请重试"
            ]
            
            for text in error_texts:
                error_element = self.browser.ele(f'xpath://div[contains(text(), "{text}")]')
                if error_element:
                    print(f"{Fore.RED}{EMOJI['ERROR']} 检测到人机验证失败信息: {text}{Style.RESET_ALL}")
                    return True
            
            # 检查是否存在验证码输入框，如果不存在可能也是验证失败
            verification_input = self.browser.ele('xpath://input[@type="text" and @inputmode="numeric"]')
            if not verification_input:
                print(f"{Fore.RED}{EMOJI['ERROR']} 未检测到验证码输入框，可能验证失败{Style.RESET_ALL}")
                return True
                
            return False
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} 检查人机验证状态时出错: {str(e)}{Style.RESET_ALL}")
            return True  # 出错时保守处理，认为验证失败

    def simulate_human_behavior(self):
        """模拟人类行为"""
        try:
            # 1. 随机鼠标移动
            elements = self.browser.eles('xpath://*')
            for _ in range(random.randint(2, 4)):
                random_element = random.choice(elements)
                self.browser.actions.move_to(random_element)
                time.sleep(random.uniform(0.3, 0.8))
            
            # 2. 随机滚动
            scroll_amounts = [100, 200, -100, -150]
            for _ in range(random.randint(1, 3)):
                scroll_amount = random.choice(scroll_amounts)
                self.browser.execute_script(f"window.scrollBy(0, {scroll_amount})")
                time.sleep(random.uniform(0.5, 1))
            
            # 3. 模拟页面浏览暂停
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"{Fore.YELLOW}{EMOJI['INFO']} 模拟人类行为时出错: {str(e)}{Style.RESET_ALL}")

    def handle_human_verification(self):
        """处理人机验证失败的情况"""
        retry_count = 0
        while retry_count < self.max_verify_retries:
            if self.check_human_verify():
                retry_count += 1
                print(f"{Fore.YELLOW}{EMOJI['WAIT']} 等待重试... ({retry_count}/{self.max_verify_retries}){Style.RESET_ALL}")
                
                # 随机等待5-15秒
                wait_time = random.uniform(5, 15)
                print(f"{Fore.CYAN}{EMOJI['INFO']} 随机等待 {wait_time:.1f} 秒...{Style.RESET_ALL}")
                time.sleep(wait_time)
                
                try:
                    # 1. 刷新页面
                    self.browser.refresh()
                    time.sleep(random.uniform(2, 4))
                    
                    # 2. 模拟人类行为
                    self.simulate_human_behavior()
                    
                    # 3. 清空所有输入框
                    input_fields = self.browser.eles('xpath://input')
                    for field in input_fields:
                        field.clear()
                        time.sleep(random.uniform(0.2, 0.5))
                    
                    # 4. 模拟人类输入行为
                    for field in input_fields:
                        # 先移动到输入框
                        self.browser.actions.move_to(field)
                        time.sleep(random.uniform(0.3, 0.7))
                        
                        # 点击输入框
                        field.click()
                        time.sleep(random.uniform(0.2, 0.5))
                        
                        # 获取字段类型
                        field_type = field.get_attribute('type')
                        if field_type == 'email':
                            # 模拟人类输入邮箱
                            for char in self.email_address:
                                field.send_keys(char)
                                time.sleep(random.uniform(0.1, 0.4))
                        elif field_type == 'text':
                            # 模拟人类输入用户名
                            for char in self.first_name:
                                field.send_keys(char)
                                time.sleep(random.uniform(0.1, 0.4))
                        
                        # 输入后的短暂暂停
                        time.sleep(random.uniform(0.5, 1))
                    
                    # 5. 再次模拟人类行为
                    self.simulate_human_behavior()
                    
                    # 6. 处理 Turnstile 验证
                    if not self.check_and_click_turnstile():
                        continue  # 如果验证失败，直接进入下一次重试
                    
                    # 7. 等待随机时间
                    time.sleep(random.uniform(2, 4))
                    
                    # 8. 移动鼠标到提交按钮并点击
                    submit_button = self.browser.ele('xpath://button[@type="submit"]')
                    if submit_button:
                        # 模拟鼠标移动轨迹
                        current_pos = self.browser.execute_script("return [window.scrollX, window.scrollY];")
                        button_pos = submit_button.rect
                        
                        # 生成随机中间点
                        mid_x = current_pos[0] + random.uniform(0, button_pos['x'])
                        mid_y = current_pos[1] + random.uniform(0, button_pos['y'])
                        
                        # 先移动到中间点
                        self.browser.execute_script(f"window.scrollTo({mid_x}, {mid_y})")
                        time.sleep(random.uniform(0.3, 0.7))
                        
                        # 再移动到按钮
                        self.browser.actions.move_to(submit_button)
                        time.sleep(random.uniform(0.5, 1))
                        
                        # 点击按钮
                        submit_button.click()
                        print(f"{Fore.GREEN}{EMOJI['REFRESH']} 重新提交表单{Style.RESET_ALL}")
                        
                        # 9. 等待并检查验证结果
                        if self.wait_for_verification_result():
                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} 人机验证通过{Style.RESET_ALL}")
                            return True
                            
                except Exception as e:
                    print(f"{Fore.RED}{EMOJI['ERROR']} 重新提交表单失败: {str(e)}{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} 人机验证通过{Style.RESET_ALL}")
                return True
                
        print(f"{Fore.RED}{EMOJI['ERROR']} 人机验证失败次数过多，请手动处理{Style.RESET_ALL}")
        return False

    def send_verification_email(self, email_address):
        """发送验证邮件"""
        try:
            print(f"{Fore.CYAN}{EMOJI['MAIL']} 发送验证邮件到 {email_address}...{Style.RESET_ALL}")
            
            # 输入邮箱地址
            email_input = self.browser.ele('xpath://input[@type="email"]')
            if email_input:
                # 清空输入框
                email_input.clear()
                # 模拟人类输入
                for char in email_address:
                    email_input.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.3))
                
                # 等待随机时间
                time.sleep(random.uniform(1, 2))
                
                # 处理 Turnstile 验证
                self.check_and_click_turnstile()
                
                # 再次等待随机时间
                time.sleep(random.uniform(1, 2))
                
                # 点击发送按钮
                send_button = self.browser.ele('xpath://button[@type="submit"]')
                if send_button:
                    # 模拟鼠标移动
                    self.browser.actions.move_to(send_button)
                    time.sleep(random.uniform(0.5, 1))
                    send_button.click()
                    
                    # 等待验证结果
                    time.sleep(2)
                    
                    # 检查是否出现人机验证失败
                    retry_count = 0
                    while retry_count < self.max_verify_retries:
                        if self.check_human_verify():
                            retry_count += 1
                            print(f"{Fore.YELLOW}{EMOJI['WAIT']} 发送验证邮件失败，等待重试... ({retry_count}/{self.max_verify_retries}){Style.RESET_ALL}")
                            
                            # 随机等待5-10秒
                            wait_time = random.uniform(5, 10)
                            print(f"{Fore.CYAN}{EMOJI['INFO']} 随机等待 {wait_time:.1f} 秒...{Style.RESET_ALL}")
                            time.sleep(wait_time)
                            
                            # 重新尝试发送
                            # 清空输入框
                            email_input.clear()
                            # 模拟人类输入
                            for char in email_address:
                                email_input.send_keys(char)
                                time.sleep(random.uniform(0.1, 0.3))
                            
                            # 处理 Turnstile 验证
                            self.check_and_click_turnstile()
                            
                            # 等待随机时间
                            time.sleep(random.uniform(2, 4))
                            
                            # 重新点击发送按钮
                            send_button = self.browser.ele('xpath://button[@type="submit"]')
                            if send_button:
                                self.browser.actions.move_to(send_button)
                                time.sleep(random.uniform(0.5, 1))
                                send_button.click()
                                time.sleep(2)
                        else:
                            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} 验证邮件发送成功{Style.RESET_ALL}")
                            return True
                    
                    if retry_count >= self.max_verify_retries:
                        print(f"{Fore.RED}{EMOJI['ERROR']} 发送验证邮件失败次数过多，请手动处理{Style.RESET_ALL}")
                        return False
                    
                else:
                    print(f"{Fore.RED}{EMOJI['ERROR']} 未找到发送按钮{Style.RESET_ALL}")
                    return False
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} 未找到邮箱输入框{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} 发送验证邮件失败: {str(e)}{Style.RESET_ALL}")
            return False 