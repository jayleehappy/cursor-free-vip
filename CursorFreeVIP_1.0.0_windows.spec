# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('turnstilePatch', 'turnstilePatch'), ('recaptchaPatch', 'recaptchaPatch'), ('uBlock0.chromium', 'uBlock0.chromium'), ('locales', 'locales'), ('images', 'images'), ('LICENSE', '.'), ('README.md', '.'), ('DEVELOPMENT_LOG.md', '.'), ('cursor_auth.py', '.'), ('reset_machine_manual.py', '.'), ('cursor_register.py', '.'), ('browser.py', '.'), ('control.py', '.'), ('.env', '.')],
    hiddenimports=['cursor_auth', 'reset_machine_manual', 'browser', 'control'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CursorFreeVIP_1.0.0_windows',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['images\\logo.png'],
)
