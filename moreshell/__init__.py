"""Start here to createMORE IPython shell magic."""

import sys
from argparse import ArgumentParser

import zetup
from decorator import decorator
from moretools import qualname
from zetup import with_arguments

from .magic import IPython_magic, IPython_cell_magic, MagicExit

zetup.toplevel(__name__, (
    'IPython_magic',
    'IPython_cell_magic',
    'MagicExit',

    # zetup.with_arrguments is so tightly bound to the IPython_magic decorator
    # for defining the magic command line arguments (just like it's used with
    # the zetup.program decorator to define the arguments of a console_script)
    # that it's also exposed here as part of the moreshell API
    'with_arguments',
))
