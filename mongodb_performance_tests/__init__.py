import os

try:
    from .settings import *
except ImportError:
    settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.py')
    raise ImportError("Can't import file with settings (%s). Please, create it using an example." % settings_path)