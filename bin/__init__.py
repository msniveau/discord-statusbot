import os, sys
__version__="0.0.1"


frozen = 'not'
if getattr(sys, 'frozen', False):
    __bundledir__ = sys._MEIPASS
else:
    __bundledir__ = os.path.dirname(os.path.abspath(__file__ + '/../'))