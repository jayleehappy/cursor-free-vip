#!/bin/bash

# 设置版本号
VERSION="1.0.0"

# 设置环境变量
export PYTHONPATH="$PWD"
export PATH="$PATH:$PWD"

# 清理旧的构建文件
echo "清理构建文件..."
rm -rf build dist *.spec

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt
pip install pyinstaller

# 获取操作系统类型
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="mac"
else
    OS_TYPE="linux"
fi

# 开始构建
echo "开始构建..."
pyinstaller --clean \
    --onefile \
    --icon=images/logo.png \
    --add-data "turnstilePatch:turnstilePatch" \
    --add-data "recaptchaPatch:recaptchaPatch" \
    --add-data "uBlock0.chromium:uBlock0.chromium" \
    --add-data "locales:locales" \
    --add-data "images:images" \
    --add-data "LICENSE:." \
    --add-data "README.md:." \
    --add-data "DEVELOPMENT_LOG.md:." \
    --add-data "cursor_auth.py:." \
    --add-data "reset_machine_manual.py:." \
    --add-data "cursor_register.py:." \
    --add-data "browser.py:." \
    --add-data "control.py:." \
    --add-data ".env:." \
    --hidden-import cursor_auth \
    --hidden-import reset_machine_manual \
    --hidden-import browser \
    --hidden-import control \
    --name "CursorFreeVIP_${VERSION}_${OS_TYPE}" \
    main.py

# 检查构建结果
if [ -f "dist/CursorFreeVIP_${VERSION}_${OS_TYPE}" ]; then
    echo -e "\n构建成功！"
    echo "可执行文件位于: dist/CursorFreeVIP_${VERSION}_${OS_TYPE}"
else
    echo -e "\n构建失败！"
fi 