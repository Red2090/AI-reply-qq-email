# main.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],  # 当前目录
    datas=[('email_config.ini', '.')],  # 包含email_config.ini文件
    binaries=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AIReplyQQEmail',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # 如果是命令行应用，保留console=True；如果是GUI应用，改为windowed=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,  # 这里引用a.datas
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AIReplyQQEmail',
)