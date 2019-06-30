"""Test :mod:`moreshell.module`."""

import sys

import pytest

from moreshell import load_magic_modules


def test_load_magic_modules(magic_module__name__, shell):
    """
    Test that :func:`moreshell.load_magic_modules` registers all ``%magic``.

    That it registers all ``%magic`` and cell ``%%magic`` created in a
    :class:`moreshell.IPython_magic_module`-wrapped module to the IPython
    shell's ``.magics_manager``

    Using full module name and therefore omitting the ``package=`` argument
    """
    assert 'test_moreshell' not in shell.magics_manager.magics['line']

    modules = load_magic_modules(magic_module__name__, shell=shell)

    from moreshell.test import magic_module
    assert sys.modules[magic_module__name__] is magic_module

    assert modules == [magic_module]
    assert shell.magics_manager.magics['line']['test_moreshell'] is (
        sys.modules[magic_module__name__].test_moreshell)


def test_load_magic_modules_with_package__name__(magic_module__name__, shell):
    """
    Test that :func:`moreshell.load_magic_modules` registers all ``%magic``.

    That it registers all ``%magic`` and cell ``%%magic`` created in a
    :class:`moreshell.IPython_magic_module`-wrapped module to the IPython
    shell's ``.magics_manager``

    Using relative module name and the ``package=`` keyword argument set to
    the parent package name
    """
    assert 'test_moreshell' not in shell.magics_manager.magics['line']

    pkgname, modname = magic_module__name__.rsplit('.', 1)
    modules = load_magic_modules(modname, package=pkgname, shell=shell)

    from moreshell.test import magic_module
    assert sys.modules[magic_module__name__] is magic_module

    assert modules == [magic_module]
    assert shell.magics_manager.magics['line']['test_moreshell'] is (
        sys.modules[magic_module__name__].test_moreshell)


def test_load_magic_modules_with_package_object(
        magic_module__name__, shell):
    """
    Test that :func:`moreshell.load_magic_modules` registers all ``%magic``.

    That it registers all ``%magic`` and cell ``%%magic`` created in a
    :class:`moreshell.IPython_magic_module`-wrapped module to the IPython
    shell's ``.magics_manager``

    Using relative module name and the ``package=`` keyword argument set to
    the parent package object
    """
    assert 'test_moreshell' not in shell.magics_manager.magics['line']

    pkgname, modname = magic_module__name__.rsplit('.', 1)
    modules = load_magic_modules(
        modname, package=sys.modules[pkgname], shell=shell)

    from moreshell.test import magic_module
    assert sys.modules[magic_module__name__] is magic_module

    assert modules == [magic_module]
    assert shell.magics_manager.magics['line']['test_moreshell'] is (
        sys.modules[magic_module__name__].test_moreshell)


def test_load_magic_modules_with_invalid_keywords(
        magic_module__name__, shell):
    """
    Test that :func:`moreshell.load_magic_modules` raises a ``TypeError``.

    When called with invalid keyword arguments
    """
    assert 'test_moreshell' not in shell.magics_manager.magics['line']

    with pytest.raises(
            TypeError,
            match=r"unexpected keyword argument\(s\) 'invalid'$"):
        load_magic_modules(magic_module__name__, shell=shell, invalid=True)


class TestIPython_magic_module(object):
    """Test :class:`moreshell.IPython_magic_module`."""

    def test_load(self, shell):
        """Test :meth:`moreshell.IPython_magic_module.load`."""
        assert 'test_moreshell' not in shell.magics_manager.magics['line']

        from moreshell.test import magic_module
        magic_module.load(shell)  # pylint: disable=no-member
        assert shell.magics_manager.magics['line']['test_moreshell'] is (
            magic_module.test_moreshell)

    def test_unload(self, shell):
        """Test :meth:`moreshell.IPython_magic_module.unload`."""
        self.test_load(shell)

        from moreshell.test import magic_module
        magic_module.unload(shell)  # pylint: disable=no-member
        assert 'test_moreshell' not in shell.magics_manager.magics['line']
