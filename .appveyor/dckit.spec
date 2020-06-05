import os
from os.path import abspath, exists, join, dirname, relpath
import platform
import sys
import warnings

cdir = abspath(".")
sys.path.insert(0, cdir)

if not exists(join(cdir, "dckit")):
	warnings.warn("Cannot find 'dckit'! Please run pyinstaller "+
                  "from git root folder.")

name = "DCKit"
pyinstdir = os.path.realpath(cdir+"/.appveyor/")
script = os.path.join(pyinstdir, name+".py")

# Icon
icofile = os.path.join(pyinstdir,"DCKit.ico")

a = Analysis([script],
             pathex=[cdir],
             hookspath=[pyinstdir],
             runtime_hooks=None)
             
options = [ ('u', None, 'OPTION'), ('W ignore', None, 'OPTION') ]

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          options,
          exclude_binaries=True,
          name=name+".exe",
          debug=False,
          strip=False,
          upx=False,
          icon=icofile,
          console=False)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name=name)
