import sys
from cx_Freeze import setup, Executable
includefiles = ["updater.ini", "icon.ico"]
packages = ["os", "sys", "threading", "subprocess", "shutil", "tempfile", "tkinter", "urllib", "traceback"]
excludes = []
includes = ["requests", "configparser", "win32api", "acl", "zipfile", "win32con", "aceutil"]


executables = [
    Executable(
	script='updater.py',
	base='Win32GUI',
	icon="icon.ico"
	)
]

setup(name='Paitent System',
      version='1.0.0.0',
      description='Python Application Updater',
	  author="AceScottie",
	  options = {'build_exe': {'includes':includes,'excludes':excludes,'packages':packages,'include_files':includefiles}}, 
      executables=executables
      )
