# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['mMultiplayerServer.py'],
             pathex=['\\\\ASUS\\Jeffrey_s_WD_Passport\\SCHOOL\\ICT\\ICT SBA\\Program\\(06072020) Final Program and Modified Report\\The Becoming of a Mathematician'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='mMultiplayerServer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
