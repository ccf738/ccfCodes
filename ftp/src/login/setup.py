'''
Created on 2013-2-20

@author: ccf
'''
from distutils.core import setup
import py2exe

setup(
    windows = [
        {
            "script": "update.py",
            "icon_resources": [(1, "Attach.ico")]
        }
    ],
)