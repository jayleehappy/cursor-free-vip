import warnings
import os
import platform
import subprocess
import time
import threading
import shutil
from logo import print_logo
from dotenv import load_dotenv
from datetime import datetime

# 忽略特定警告
warnings.filterwarnings("ignore", category=SyntaxWarning)

class LoadingAnimation:
    def __init__(self):
        self.is_running = False
        self.animation_thread = None

    def start(self, message="Building"):
        self.is_running = True
        self.animation_thread = threading.Thread(target=self._animate, args=(message,))
        self.animation_thread.start()

    def stop(self):
        self.is_running = False
        if self.animation_thread:
            self.animation_thread.join()
        print("\r" + " " * 70 + "\r", end="", flush=True)

    def _animate(self, message):
        animation = "|/-\\"
        idx = 0
        while self.is_running:
            print(f"\r{message} {animation[idx % len(animation)]}", end="", flush=True)
            idx += 1
            time.sleep(0.1)

def progress_bar(progress, total, prefix="", length=50):
    filled = int(length * progress // total)
    bar = "█" * filled + "░" * (length - filled)
    percent = f"{100 * progress / total:.1f}"
    print(f"\r{prefix} |{bar}| {percent}% Complete", end="", flush=True)
    if progress == total:
        print()

def simulate_progress(message, duration=1.0, steps=20):
    print(f"\033[94m{message}\033[0m")
    for i in range(steps + 1):
        time.sleep(duration / steps)
        progress_bar(i, steps, prefix="Progress:", length=40)

def clean_build():
    """清理构建文件夹"""
    dirs_to_clean = ['build', 'dist']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理目录: {dir_name}")
    
    for file_pattern in files_to_clean:
        for file in os.listdir('.'):
            if file.endswith('.spec'):
                os.remove(file)
                print(f"已删除文件: {file}")

def build_exe():
    """构建exe文件"""
    try:
        # 清理旧的构建文件
        clean_build()
        
        # 获取版本号
        version = "1.0.0"  # 你可以从其他地方读取版本号
        
        # 构建命令
        build_cmd = f"pyinstaller --clean --onefile --icon=images/logo.png --name=cursor-free-vip-{version} main.py"
        
        # 添加数据文件
        build_cmd += " --add-data 'locales/*.json;locales'"
        build_cmd += " --add-data 'images/*.png;images'"
        build_cmd += " --add-data 'LICENSE;.'"
        build_cmd += " --add-data 'README.md;.'"
        build_cmd += " --add-data 'DEVELOPMENT_LOG.md;.'"
        
        # 执行构建
        print("开始构建...")
        os.system(build_cmd)
        
        # 检查构建结果
        dist_dir = "dist"
        if os.path.exists(dist_dir) and os.listdir(dist_dir):
            print("\n构建成功!")
            print(f"可执行文件位于: {dist_dir}")
        else:
            print("\n构建失败!")
            
    except Exception as e:
        print(f"\n构建过程中出错: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    if build_exe():
        print("\n打包完成!") 