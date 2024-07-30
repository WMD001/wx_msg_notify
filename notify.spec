# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('wcferry', 'wcferry'), ('assets', '.')],
    hiddenimports=['_cffi_backend'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='notify',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\notify.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='notify',
)

import shutil
import os

def create_logs_directory():
    logs_path = os.path.join('dist', 'notify', 'logs')
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

# Call the function to create the logs directory
create_logs_directory()

def copy_assets_directory():
    source = os.path.join(os.getcwd(), 'assets')
    destination = os.path.join('dist', 'notify', 'assets')
    if os.path.exists(source):
        shutil.copytree(source, destination)

# Call the function to copy the assets directory
copy_assets_directory()