# Cursor Free VIP

## 项目说明
这是一个基于 [yeongpin/cursor-free-vip](https://github.com/yeongpin/cursor-free-vip) 项目的改进版本。
感谢原作者 yeongpin 提供的基础项目框架。

## 主要改进
1. 人机验证优化
   - 增加多重验证失败检测机制
   - 改进表单重填功能，模拟真实人类操作
   - 优化验证码处理流程
   - 添加详细的状态提示

2. 账号管理功能
   - 自动保存注册账号信息到 cursor_accounts.txt
   - 实现账号自动切换功能
   - 优化账号信息展示

3. 错误处理增强
   - 完善 SSL 握手错误处理
   - 添加网络状态检测
   - 优化重试机制
   - 改进错误提示信息

4. 界面优化
   - 添加更详细的操作提示
   - 优化状态显示效果
   - 改进多语言支持

## 使用方法
1. 环境要求
   - Python 3.7+
   - Chrome 浏览器
   - Windows 10/11 或 macOS

2. 安装步骤
   ```bash
   # 克隆项目
   git clone https://github.com/jayleehappy/cursor-free-vip.git
   cd cursor-free-vip
   
   # 安装依赖
   pip install -r requirements.txt
   ```

3. 运行程序
   ```bash
   python main.py
   ```

4. 功能选项
   - 注册 Cursor 账号
   - 重置机器码
   - 退出 Cursor
   - 切换语言

## 注意事项
1. 注册过程
   - 确保网络稳定，避免频繁断开
   - 注册时请耐心等待人机验证
   - 验证失败时会自动重试，无需手动操作
   - 最多重试3次，超过后需手动处理

2. 账号管理
   - 账号信息自动保存在 cursor_accounts.txt
   - 切换账号时会自动退出并重启 Cursor
   - 请妥善保管账号信息文件

3. 安全提示
   - 请勿频繁注册账号
   - 建议使用真实邮箱注册
   - 遵守 Cursor 使用条款
   - 定期更新程序以获取最新优化

## 常见问题
1. SSL握手错误
   - 检查网络连接是否稳定
   - 确认系统时间是否准确
   - 尝试重新运行程序

2. 人机验证失败
   - 等待几分钟后再试
   - 检查网络连接
   - 确保未使用代理或VPN

3. 账号切换问题
   - 确保 Cursor 已完全退出
   - 检查账号信息是否正确
   - 等待几秒后再尝试切换

## 更新日志
请查看 [DEVELOPMENT_LOG.md](./DEVELOPMENT_LOG.md) 了解详细更新记录。

---

# ➤ Original Project | 原项目

<div align="center">
<p align="center">
  <img src="./images/logo.png" alt="Cursor Pro Logo" width="200"/>
</p>

<p align="center">

[![Release](https://img.shields.io/github/v/release/yeongpin/cursor-free-vip?style=flat-square&logo=github&color=blue)](https://github.com/yeongpin/cursor-free-vip/releases/latest)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC_BY--NC--ND_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
[![Stars](https://img.shields.io/github/stars/yeongpin/cursor-free-vip?style=flat-square&logo=github)](https://github.com/yeongpin/cursor-free-vip/stargazers)

</p>

This is a tool to automatically register (except for Google verification code), support Windows and macOS systems, complete Auth verification, and reset Cursor's configuration.

這是一個自動化工具，自動註冊（除了Google驗證碼)，支持 Windows 和 macOS 系統，完成Auth驗證，重置Cursor的配置。

<p align="center">
  <img src="./images/new107_2025-01-15_13-53-56.png" alt="new" width="400"/><br>
</p>

<br>
<p align="center">
  <img src="./images/free_2025-01-14_14-59-15.png" alt="free" width="400"/><br>
</p>

## ⚠️ Google Recaptcha need to be manually verified, don't be lazy, move your fingers, verify it, otherwise it will keep prompting you to verify ⚠️
### If you dont have google chrome , you can download it from [here](https://www.google.com/intl/en_pk/chrome/)

## ⚠️ 郵箱驗證 需要手動驗證，不要那麼懶，動一動手指，驗證一下，不然會一直提示你驗證 ⚠️
### 如果沒有Google Chrome，可以從[這裡](https://www.google.com/intl/en_pk/chrome/)下載

</p>
</div>


## 🔄 更新日志
<details open>
<summary>v1.0.7 - HotFix</summary>

1. Fix Reset Machine | 修復重置機器
2. Fix Locale Language | 修復多語言
</details>
<details>
<summary>Other Version Change Log</summary>
<details>
<summary>v1.0.7</summary>

1. Add Locale Language Support | 增加多語言支持
<p align="center">
  <img src="./images/locale_2025-01-15_13-40-08.png" alt="locale" width="400"/><br>
</p>
</details>
<details>
<summary>v1.0.6</summary>

1. Add Quit Cursor Option | 增加退出Cursor選項
2. Add Recaptcha Path Patch | 增加Recaptcha路徑修復
3. Fix Admin Permission | 修復管理員權限問題
4. Remove all need admin permission | 移除所有需要管理員權限
</details>
<details>
<summary>v1.0.5 - HotFix</summary>

1. Fix: Mac Browser Control | 修復Mac瀏覽器控制問題
2. Fix: Verification Code Cant Patch | 修復驗證碼無法修復問題
3. Add Linux Support | 增加Linux支持
<p align="center">
  <img src="./images/fix_2025-01-14_21-30-43.png" alt="fix" width="400"/><br>
</p>
</details>
<details>
<summary>v1.0.5</summary>

1. Remove MachineID | 移除機器碼ID
2. Change to automatic registration account | 全面改為自動註冊賬號
3. Use your own exclusive new account | 使用自己獨享的新賬號
4. Fully automatic reset machine configuration | 全面自動化重置機器配置
<p align="center">
  <img src="./images/pro_2025-01-14_14-40-37.png" alt="Why" width="400"/><br>
</p>
</details>
<details>
<summary>v1.0.4</summary>

1. Fix: Cursor's configuration | 修復Cursor的配置問題
2. Fix Cloud Lame | 修復雲端慢速模式
</details>
<details>
<summary>v1.0.3</summary>

1. Fix: Cursor's configuration | 修復Cursor的配置問題
2. Add Manual Reset Machine | 增加手動重置機器
3. Add CDN Cloud Control WatchDog | 增加CDN雲端控制WatchDog
4. Add Mac OS Support | 增加Mac OS支持
5. 759 ++ People use , but star only a few | 759 ++人使用，但只有幾個人點贊
<p align="center">
  <img src="./images/what_2025-01-13_13-32-54.png" alt="Why" width="400"/><br>
</p>
</details>
<details>
<summary>v1.0.2</summary>
  
1. Fix: Some known issues | 修復了一些已知問題
2. Add cloud control device code | 增加雲端控制設備碼
3. Cloud reset device code | 雲端重置設備碼
4. Remove official WatchDog monitoring | 移除官方WatchDog監控
5. Remove Proxy official prompt | 移除Proxy 官方提示
6. Fix: Too Many Computer | 修復Too Many Computer 問題
7. Fix Billing Issue | 修復計費問題
8. Fix: Cursor's configuration | 修復Cursor的配置問題
9. Fix cursor-slow mode | 修復cursor-slow模式
</details>
<details>
<summary>v1.0.1</summary>

1. Fix: Reset machine ID | 修復了重置機器ID的問題
2. Fix: Bypass membership check | 修復了 繞過會員檢查的問題
3. Fix: Auto upgrade to "pro" membership | 修復了 自動升級為pro會員的問題
4. Fix: Real-time send Token request | 修復了 實時發送Token請求的問題
5. Fix: Reset Cursor's configuration | 修復了 重置Cursor的配置的問題
</details>

<details>
<summary>v1.0</summary>
1. Preview Image | 預覽圖<br>
<p align="center">
  <img src="./images/pro_2025-01-11_00-50-40.png" alt="Cursor Pro Logo" width="400"/><br>
</p>
<p align="center">
  <img src="./images/pro_2025-01-11_00-51-07.png" alt="Cursor Pro Logo" width="400"/><br>
</p>
2. Add usage period,but can be contacted by leaving MachineID | 不得已才添加，但可以通過留下MachineID 聯繫作者
<br>

<p align="center">
  <img src="./images/pro_2025-01-11_16-24-03.png" alt="Cursor Pro Logo" width="400"/><br>
</p>
</details>
</details>

## ✨ Features | 功能特點

* Automatically register Cursor membership<br>自動註冊Cursor會員<br>

* Except for Google verification code<br>除了Google驗證碼<br>

* Support Windows and macOS systems<br>支持 Windows 和 macOS 系統<br>

* Complete Auth verification<br>完成Auth驗證<br>

* Reset Cursor's configuration<br>重置Cursor的配置<br>


## 💻 System Support | 系統支持

|Windows|x64|✅|macOS|Intel|✅|
|:---:|:---:|:---:|:---:|:---:|:---:|
|Windows|x86|✅|macOS|Apple Silicon|✅|
|Linux|x64|✅|Linux|x86|✅|
|Linux|ARM64|✅|Linux|ARM64|✅|

## 👀 How to use | 如何使用
|⚠️Must logout your account before running the script⚠️|⚠️必須先登出你的帳戶再運行腳本⚠️ |
|:---:|:---:|
<br>
<details open>
<summary><b>⭐ Auto Run Script | 腳本自動化運行</b></summary>

**Linux/macOS**
```bash
curl -fsSL https://raw.githubusercontent.com/yeongpin/cursor-free-vip/main/scripts/install.sh -o install.sh && chmod +x install.sh && ./install.sh
```

**Windows**
```powershell
irm https://raw.githubusercontent.com/yeongpin/cursor-free-vip/main/scripts/install.ps1 | iex
```
</details>

<details>
<summary><b>⭐ Manual Reset Machine | 手動運行重置機器</b></summary>

**Linux/macOS**
```bash
curl -fsSL https://raw.githubusercontent.com/yeongpin/cursor-free-vip/main/scripts/reset.sh | sudo bash
```

**Windows**
```powershell
irm https://raw.githubusercontent.com/yeongpin/cursor-free-vip/main/scripts/reset.ps1 | iex
```
</details>

2. If you want to stop the script, please press Ctrl+C<br>要停止腳本，請按 Ctrl+C

## ❗ Note | 注意事項

* Confirm that Cursor is closed before running the script <br>請確保在運行腳本前已經關閉 Cursor<br>

* Do not close this script when using Cursor <br>使用Cursor時請勿關閉此腳本<br>

* This tool is only for learning and research purposes <br>此工具僅供學習和研究使用<br>

* Please comply with the relevant software usage terms when using this tool <br>使用本工具時請遵守相關軟件使用條款



## 🚨 Common Issues | 常見問題

|如果遇到權限問題，請確保：|If you encounter permission issues, please ensure:|
|:---:|:---:|
| 此腳本以管理員身份運行 | This script is run with administrator privileges |



## 🤩 Contribution | 貢獻

歡迎提交 Issue 和 Pull Request！



## 📩 Disclaimer | 免責聲明

本工具僅供學習和研究使用，使用本工具所產生的任何後果由使用者自行承擔。 <br>

源代碼靈感來之 | Original code inspiration from [Here](https://github.com/hmhm2022/gpt-cursor-auto)

This tool is only for learning and research purposes, and any consequences arising from the use of this tool are borne by the user.

## License
MIT License
