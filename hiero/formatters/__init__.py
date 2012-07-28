import os
import sys
import glob

import inspect

def load_modules(filemask='*.py', ignore_list=('__init__.py', )):
    """
    This loads all modules from the formatters directory
    """
    modules = {}
    dirname = os.path.dirname(__file__)

    if dirname:
        filemask = os.path.join(dirname, filemask)

    for fn in glob.glob(filemask):
        fn = os.path.split(fn)[1]

        if fn in ignore_list:
            continue

        fn = os.path.splitext(fn)[0]
        modules[fn] = __import__(fn, globals(), locals())

    return modules


def get_formatter(formatter_class):
    """
    This will generate HTML for a specific markup language but will not
    highlight source code
    """
    cls = ''

    if formatter_class == 'rst':
        cls = 'RestructuredTextFormatter'
    elif formatter_class == 'markdown':
        cls = 'MarkdownFormatter'

    load_modules()
    current_module = sys.modules[__name__]
    formatter = get_module_classes(current_module, cls)

    return formatter


def get_module_classes(module, formatter_class):
    """
    Recursively searches through all modules looking for the class
    that we are asking for
    """
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__name__ == formatter_class:
            return obj

    # Didn't find the class we want on that module, loop thorugh
    # its child modules
    for name, obj in inspect.getmembers(module, inspect.ismodule):
        if obj.__name__.startswith(__name__):
            cls = get_module_classes(obj, formatter_class)

            if cls:
                return cls
