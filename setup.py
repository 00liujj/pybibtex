from distutils.core import setup
import py2exe
import sys

sys.argv.extend(['py2exe', '-p' 'pybtex'])
print sys.argv

options = { 'py2exe': {
        'optimize':2,
        'bundle_files': 1,
        #'skip_archive' : True,
        #'compressed': True
        }}


setup(console = ["pybibtex.py"], options = options)
