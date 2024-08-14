# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('back.png', '.'),
        ('c1.png', '.'),
        ('c2.png', '.'),
        ('c3.png', '.'),
        ('c4.png', '.'),
        ('calcular_cocomo81.png', '.'),
        ('calcular_cocomoII.png', '.'),
        ('cpm.png', '.'),
        ('esf_cocomo_ii.png', '.'),
        ('esf_cocomo_inter_i.png', '.'),
        ('guardar.png', '.'),
        ('info.png', '.'),
        ('puntos.ui', '.'),
        ('cocomop.ui', '.'),
        ('cocopost.ui', '.'),
        ('ecuaciones.ui', '.'),
        ('ecuaciones_cocomo_ii.ui', '.'),
        ('principal.ui', '.'),
        ('tabla.png', '.'),
        ('tiempo_cocomo_ii.png', '.'),
        ('tiempo_cocomo_inter_i.png', '.')
],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    exclude_binaries=True,
    name='Software_de_Estimacion',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Software_de_Estimacion'
)