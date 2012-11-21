from distutils.core import setup
import py2exe

setup(name = "pyRDC",
zipfile = None,
  options = { "py2exe": { "bundle_files": 1,
                          "dll_excludes": ["w9xpopen.exe","msvcp90.dll"],
                          "includes": ["PySide.QtXml"],
                          "compressed": 1,
                          "optimize": 2,
                          "dist_dir": "bin"}},
              windows=[{"script": "pyRdc.py"}]
  )