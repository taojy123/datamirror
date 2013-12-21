# -*- mode: python -*-
a = Analysis(['datamirror.py'],
             pathex=['E:\\Workspace\\datamirror'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'datamirror.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
