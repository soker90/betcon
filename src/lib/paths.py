"""Path utilities for handling PyInstaller bundled resources"""
import os
import sys
import inspect


def get_base_dir():
    """Get base directory - works for both development and PyInstaller bundle"""
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        # sys._MEIPASS points to the temp extraction directory
        # Files are in sys._MEIPASS/ui/, sys._MEIPASS/assets/, etc.
        # Code expects to do directory + "/../ui/file.ui"
        # So we return sys._MEIPASS + "/src" (which doesn't exist but that's OK)
        # Then src/../ui/ = ui/ within _MEIPASS
        return os.path.join(sys._MEIPASS, 'src')
    else:
        # Running in development - get caller's directory
        frame = inspect.currentframe().f_back
        caller_file = inspect.getfile(frame)
        return os.path.realpath(os.path.abspath(os.path.dirname(caller_file)))
