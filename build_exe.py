import os
import shutil
import subprocess
import sys

def clean_build():
    """清理构建文件"""
    print("清理构建文件...")
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            os.remove(file)

def install_dependencies():
    """安装依赖"""
    print("安装依赖...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_exe():
    """构建可执行文件"""
    version = "1.0.0"
    print("开始构建...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--onefile",
        "--icon=images/logo.png",
        f"--name=CursorFreeVIP_{version}_windows",
        "--add-data", "turnstilePatch;turnstilePatch",
        "--add-data", "recaptchaPatch;recaptchaPatch",
        "--add-data", "uBlock0.chromium;uBlock0.chromium",
        "--add-data", "locales;locales",
        "--add-data", "images;images",
        "--add-data", "LICENSE;.",
        "--add-data", "README.md;.",
        "--add-data", "DEVELOPMENT_LOG.md;.",
        "--add-data", "cursor_auth.py;.",
        "--add-data", "reset_machine_manual.py;.",
        "--add-data", "cursor_register.py;.",
        "--add-data", "browser.py;.",
        "--add-data", "control.py;.",
        "--add-data", ".env;.",
        "--hidden-import=cursor_auth",
        "--hidden-import=reset_machine_manual",
        "--hidden-import=browser",
        "--hidden-import=control",
        "main.py"
    ]
    
    subprocess.check_call(cmd)
    
    # 检查构建结果
    exe_path = f"dist/CursorFreeVIP_{version}_windows.exe"
    if os.path.exists(exe_path):
        print("\n构建成功！")
        print(f"可执行文件位于: {exe_path}")
    else:
        print("\n构建失败！")

def main():
    try:
        clean_build()
        install_dependencies()
        build_exe()
    except Exception as e:
        print(f"\n构建过程中出错: {str(e)}")
        return False
    return True

if __name__ == "__main__":
    main()
    input("按任意键继续...") 