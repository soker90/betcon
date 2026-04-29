# -*- mode: python ; coding: utf-8 -*-
# Especificación optimizada para Linux: numpy excluido (se usa del sistema)
import os
import sys
from pathlib import Path

block_cipher = None

# Rutas base
root_dir = Path.cwd()
src_dir = root_dir / 'src'
assets_dir = root_dir / 'assets'
resources_dir = root_dir / 'resources'
lang_dir = root_dir / 'lang'
ui_dir = root_dir / 'ui'
default_dir = root_dir / 'default'

# Datos a incluir
datas = [
    (str(assets_dir), 'assets'),
    (str(ui_dir), 'ui'),
    (str(lang_dir / 'mo'), 'lang/mo'),
    (str(default_dir / 'database.sql'), 'default'),
    (str(resources_dir / 'bookies'), 'resources/bookies'),
    (str(resources_dir / 'sports'), 'resources/sports'),
    (str(resources_dir / 'icon.png'), 'resources'),
    (str(src_dir / 'version.txt'), '.'),
]

# Imports ocultos para PySide6 y librerías pequeñas que pueden no estar en todas las distribuciones
hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'PySide6.QtSvg',
]

a = Analysis(
    [str(src_dir / 'Betcon')],
    pathex=[str(src_dir), str(src_dir / 'lib')],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'pandas',
        'scipy',
        'jupyter',
        'notebook',
        'IPython',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='betcon',
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
    icon=str(resources_dir / 'icon.png') if (resources_dir / 'icon.png').exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='betcon',
)
