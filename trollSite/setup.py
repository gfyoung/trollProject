
from setuptools import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [{'script': 'trollApp/customTrollCode/code/tmpFile_1435724262.py'}],
    zipfile = None
)
