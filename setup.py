# cmd v mapi, kjer mas vse:
# C:/python27/python setup.py py2exe

from distutils.core import setup
import py2exe

setup(
    windows = [
        {
            "script": "calendar.pyw",
            "icon_resources": [(1, "Calendar.ico")]
        }
    ],
)
