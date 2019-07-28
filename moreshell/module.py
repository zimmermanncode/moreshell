"""Wrap modules for creating ``%magic`` inside."""

import sys
from importlib import import_module
from inspect import ismodule

import zetup
from moretools import dictkeys

import moreshell
from .magic import IPython_magic, IPython_cell_magic, magic_function

zetup.module(__name__, [
    'IPython_magic_module',
    'load_magic_modules',
])


class IPython_magic_module(zetup.module):
    """
    Wrapper for modules defining new ``%magic`` and cell ``%%magic``.

    Just instantiate it in the beginning of such a module like shown in
    :mod:`moreshell.test.magic_module` ::

        from moreshell import IPython_magic_module

        IPython_magic_module(__name__, [
            'test_moreshell',
        ])

    The wrapper is based on ``zetup.module`` and takes the same two basic
    arguments:

    -   The ``__name__`` of the wrapped module
    -   The module's API names that would normally be defined in ``__all__``.
        In the case of this wrapper type, they are essentially the names of
        the IPython ``%magic`` functions defined in the module

    The wrapped module then features :meth:`.load` and :meth:`.unload` to
    dynamically add or remove from IPython's ``magics_manager`` all the
    ``%magic`` and cell ``%%magic`` functions of the module, meaning all the
    functions which are defined using the :func:`moreshell.IPython_magic` and
    :func:`moreshell.IPython_cell_magic` decorators, respectively
    """

    __package__ = moreshell

    def load(self, shell):
        for name in self.__all__:
            obj = getattr(self, name)
            if isinstance(obj, magic_function):
                obj.load(shell=shell)

    def unload(self, shell):
        for name in self.__all__:
            obj = getattr(self, name)
            if isinstance(obj, magic_function):
                obj.unload(shell=shell)


def load_magic_modules(*names, **kwargs):
    """
    Use in ``load_ipython_extension`` functions.

    To load your project's :class:`moreshell.IPython_magic_module`-based
    modules, where all the new ``%magic`` and cell ``%%magic`` is defined

    :param names:
        The names of the magic modules to load
    :param kwargs:
        -   `package=`
            The optional parent package name of the modules
        -   `shell=`
            The IPython shell instance given to ``load_ipython_extension``
    """
    package = kwargs.pop('package', None)
    shell = kwargs.pop('shell', None)
    if kwargs:
        raise TypeError(
            "moreshell.load_magic_modules() "
            "got (an) unexpected keyword argument(s) {}"
            .format(', '.join(map(repr, dictkeys(kwargs)))))

    modules = import_magic_modules(names, package=package)
    for mod in modules:
        mod.load(shell=shell)
    return modules


def import_magic_modules(names, package=None):
    """
    Import modules wrapped with :class:`moreshell.IPython_magic_module`.

    :param names:
        The names of the magic modules to load
    :param package:
        The optional parent package name of the modules
    """
    if package is not None:
        if ismodule(package):
            package = package.__name__
        names = ('.'.join((package, name)) for name in names)

    modules = []
    for name in names:
        mod = import_module(name)
        if not isinstance(mod, IPython_magic_module):
            raise TypeError(
                "{!r} is not wrapped with {!r}".format(
                    mod, IPython_magic_module))

        modules.append(mod)
    return modules
