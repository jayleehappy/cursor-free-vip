@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: 设置版本号
set VERSION=1.0.0

:: 设置环境变量
set "PYTHONPATH=%CD%"
set "PATH=%PATH%;%CD%"

:: 清理旧的构建文件
echo 清理构建文件...
if exist "build" rd /s /q "build"
if exist "dist" rd /s /q "dist"
del /f /q *.spec 2>nul

:: 安装依赖
echo 安装依赖...
python -m pip install -r requirements.txt
python -m pip install pyinstaller

:: 开始构建
echo 开始构建...
python -m PyInstaller --clean ^
    --onefile ^
    --icon="images/logo.png" ^
    --add-data "turnstilePatch;turnstilePatch" ^
    --add-data "recaptchaPatch;recaptchaPatch" ^
    --add-data "uBlock0.chromium;uBlock0.chromium" ^
    --add-data "locales;locales" ^
    --add-data "images;images" ^
    --add-data "LICENSE;." ^
    --add-data "README.md;." ^
    --add-data "DEVELOPMENT_LOG.md;." ^
    --add-data "cursor_auth.py;." ^
    --add-data "reset_machine_manual.py;." ^
    --add-data "cursor_register.py;." ^
    --add-data "browser.py;." ^
    --add-data "control.py;." ^
    --add-data ".env;." ^
    --hidden-import=cursor_auth ^
    --hidden-import=reset_machine_manual ^
    --hidden-import=browser ^
    --hidden-import=control ^
    --name "CursorFreeVIP_%VERSION%_windows" ^
    main.py

:: 检查构建结果
if exist "dist\CursorFreeVIP_%VERSION%_windows.exe" (
    echo.
    echo 构建成功！
    echo 可执行文件位于: dist\CursorFreeVIP_%VERSION%_windows.exe
) else (
    echo.
    echo 构建失败！
)

pause 