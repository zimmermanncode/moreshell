"""Test :mod:`moreshell.magic`."""

from textwrap import dedent

import pytest

from moreshell import (
    IPython_magic, IPython_cell_magic, IPythonMagicExit, with_arguments)
from moreshell.magic import magic_function


class Test_magic_function(object):
    """Test the basic abstract :class:`moreshell.magic.magic_function`."""

    def test__init__fails(self):
        """Test that direct instantiation of the abstract base class fails."""
        def func(shell, args):  # pragma: no cover
            func.was_not_called = False

        func.was_not_called = True

        with pytest.raises(
                TypeError, match=r"^Can't instantiate abstract class"):
            magic_function(func)

        # Also check that func doesn't get called
        assert func.was_not_called


class TestIPython_magic(object):
    """
    Test the :class:`moreshell.IPython_magic` decorator.

    And test the ``%magic`` and cell ``%%magic`` functions created with it
    """

    def test__call__with_invalid_kind_of_magic(self):
        """
        Test that an ``AssertionError`` is raised.

        When the internal ``kind_of_magic`` argument is used improperly
        """
        def magic(shell, args):  # pragma: no cover
            pass

        with pytest.raises(
                AssertionError,
                match=r" 'line' or 'cell', not: 'invalid'$"):

            magic_deco = IPython_magic(with_arguments('-f', '--flag'))
            magic_deco(magic, kind_of_magic='invalid')

    def test_magic__help(self, capsys):
        """
        Test the ``--help`` output of a created ``%magic``.

        And test that a :exc:`moreshell.MagicExit` with code ``0`` is raised
        """
        @IPython_magic(with_arguments('value')('-f', '--flag'))
        def magic(shell, args):  # pragma: no cover
            magic.was_not_called = False

        magic.was_not_called = True

        with pytest.raises(IPythonMagicExit, match=r'^0$') as exc:
            magic('--help')  # pylint: disable=no-value-for-parameter
        assert exc.value.code == 0

        # Also, due to the exception, the decorated function should not get
        # called
        assert magic.was_not_called

        std = capsys.readouterr()
        assert std.out == dedent("""
        usage: %magic [-h] [-f FLAG] value

        positional arguments:
          value

        optional arguments:
          -h, --help            show this help message and exit
          -f FLAG, --flag FLAG
        """).lstrip()
        assert std.err == ""

    def test_magic__doc__(self, capsys):
        """
        Test the ``.__doc__`` property of a created ``%magic``.

        The ``--help`` output of the ``%magic`` should be printed

        And test that a :exc:`moreshell.MagicExit` with code ``0`` is raised
        """
        @IPython_magic(with_arguments('value')('-f', '--flag'))
        def magic(shell, args):  # pragma: no cover
            magic.was_not_called = False

        magic.was_not_called = True

        with pytest.raises(IPythonMagicExit, match=r'^0$') as exc:
            assert magic.__doc__ is None
        assert exc.value.code == 0

        # Also, due to the exception, the decorated function should not get
        # called
        assert magic.was_not_called

        std = capsys.readouterr()
        assert std.out == dedent("""
        usage: %magic [-h] [-f FLAG] value

        positional arguments:
          value

        optional arguments:
          -h, --help            show this help message and exit
          -f FLAG, --flag FLAG
        """).lstrip()
        assert std.err == ""

    def test_cell_magic__help(self, capsys):
        """
        Test the ``--help`` output of an accompanying cell ``%%magic``.

        And test that a :exc:`moreshell.MagicExit` with code ``0`` is raised
        """
        @IPython_magic(with_arguments('value')('-f', '--flag'))
        def magic(shell, args):  # pragma: no cover
            pass

        @magic.cell_magic
        def magic(shell, args, block):  # pragma: no cover
            magic.cell.was_not_called = False

        magic.cell.was_not_called = True

        with pytest.raises(IPythonMagicExit, match=r'^0$') as exc:
            magic.cell('--help', block="")
        assert exc.value.code == 0

        # Also, due to the exception, the decorated function should not get
        # called
        assert magic.cell.was_not_called

        std = capsys.readouterr()
        assert std.out == dedent("""
        usage: %%magic [-h] [-f FLAG] value

        positional arguments:
          value

        optional arguments:
          -h, --help            show this help message and exit
          -f FLAG, --flag FLAG
        """).lstrip()
        assert std.err == ""

    def test_cell_magic__doc__(self, capsys):
        """
        Test the ``.__doc__`` property of a accompanying cell ``%%magic``.

        The ``--help`` output of the cell ``%%magic`` should be printed

        And test that a :exc:`moreshell.MagicExit` with code ``0`` is raised
        """
        @IPython_magic(with_arguments('value')('-f', '--flag'))
        def magic(shell, args):  # pragma: no cover
            pass

        @magic.cell_magic
        def magic(shell, args, block):  # pragma: no cover
            magic.cell.was_not_called = False

        magic.cell.was_not_called = True

        with pytest.raises(IPythonMagicExit, match=r'^0$') as exc:
            assert magic.cell.__doc__ is None
        assert exc.value.code == 0

        # Also, due to the exception, the decorated function should not get
        # called
        assert magic.cell.was_not_called

        std = capsys.readouterr()
        assert std.out == dedent("""
        usage: %%magic [-h] [-f FLAG] value

        positional arguments:
          value

        optional arguments:
          -h, --help            show this help message and exit
          -f FLAG, --flag FLAG
        """).lstrip()
        assert std.err == ""


class TestIPython_cell_magic(object):
    """
    Test the :class:`moreshell.IPython_cell_magic` decorator.

    And the cell ``%%magic`` functions created with it
    """

    def test_magic__help(self, capsys):
        """
        Test the ``--help`` output of a created cell ``%%magic``.

        And that a :exc:`moreshell.MagicExit` with code ``0`` is raised
        """
        @IPython_cell_magic(with_arguments('-f', '--flag'))
        def magic(shell, args, block):  # pragma: no cover
            magic.was_not_called = False

        magic.was_not_called = True

        with pytest.raises(IPythonMagicExit, match=r'^0$') as exc:
            magic('--help', block="")  # pylint: disable=no-value-for-parameter
        assert exc.value.code == 0

        # Also, due to the exception, the decorated function should not get
        # called
        assert magic.was_not_called

        std = capsys.readouterr()
        assert std.out == dedent("""
        usage: %%magic [-h] [-f FLAG]

        optional arguments:
          -h, --help            show this help message and exit
          -f FLAG, --flag FLAG
        """).lstrip()
        assert std.err == ""

    def test_magic__doc__(self, capsys):
        """
        Test the ``.__doc__`` property of a created cell ``%%magic``.

        The ``--help`` output of the cell ``%%magic`` should be printed

        And test that a :exc:`moreshell.MagicExit` with code ``0`` is raised
        """
        @IPython_cell_magic(with_arguments('-f', '--flag'))
        def magic(shell, args):  # pragma: no cover
            magic.was_not_called = False

        magic.was_not_called = True

        with pytest.raises(IPythonMagicExit, match=r'^0$') as exc:
            assert magic.__doc__ is None
        assert exc.value.code == 0

        # Also, due to the exception, the decorated function should not get
        # called
        assert magic.was_not_called

        std = capsys.readouterr()
        assert std.out == dedent("""
        usage: %%magic [-h] [-f FLAG]

        optional arguments:
          -h, --help            show this help message and exit
          -f FLAG, --flag FLAG
        """).lstrip()
        assert std.err == ""
