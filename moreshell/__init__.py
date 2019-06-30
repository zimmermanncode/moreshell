"""Start here to createMORE IPython shell magic."""

import sys
from argparse import ArgumentParser
from importlib import import_module
from inspect import ismodule

import zetup
from decorator import decorator
from moretools import dictkeys, qualname
from zetup import with_arguments

from .magic import IPython_magic, IPython_cell_magic, IPythonMagicExit
from .module import IPython_magic_module, load_magic_modules


zetup.toplevel(__name__, (
    'IPython_cell_magic',
    'IPython_magic',
    'IPython_magic_module',
    'IPythonMagicExit',
    'load_magic_modules',

    # zetup.with_arrguments is so tightly bound to the IPython_magic decorator
    # for defining the magic command line arguments (just like it's used with
    # the zetup.program decorator to define the arguments of a console_script)
    # that it's also exposed here as part of the moreshell API
    'with_arguments',
))
