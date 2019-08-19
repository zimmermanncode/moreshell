"""The fancy decorator way of defining new ``%magic`` functions."""

from abc import ABCMeta, abstractproperty

import zetup
from six import with_metaclass

import moreshell

__all__ = ('IPython_magic', 'IPython_cell_magic', 'IPythonMagicExit')


class IPythonMagicExit(SystemExit):
    """
    A :class:`moreshell.IPython_magic`-based ``%magic`` raised ``SystemExit``.

    Which happens when the underlying ``argparse.ArgumentParser.parse_args``
    fails or prints the ``--help`` output
    """

    __package__ = moreshell


class magic_function_meta(ABCMeta, zetup.meta):
    """Metaclass for :class:`moreshell.magic.magic_function`."""

    def __init__(cls, clsname, bases, clsattrs):
        """
        Create a ``.__doc__`` property for every ``%magic``.

        To get the ``--help`` output when using ``%magic?`` in IPython
        """
        ABCMeta.__init__(cls, clsname, bases, clsattrs)
        zetup.meta.__init__(cls, clsname, bases, clsattrs)

        def __doc__(self):
            """Print the ``--help`` output of this ``%magic``."""
            self.creator.parse_args(['--help'])

        cls.__doc__ = property(__doc__)


class magic_function(with_metaclass(magic_function_meta, zetup.object)):
    """
    Abstract base class for ``%magic`` and cell ``%%magic`` functions.

    Which are created with :class:`moreshell.IPython_magic` and
    :class:`moreshell.IPython_cell_magic`, respectively.
    """

    #:  It's a kind of magic.
    #
    #   There can be only two: ``'line'`` or ``'cell'``
    kind_of_magic = 'line'

    #: The IPython shell instance, which is assigned by :meth:`.load`.
    shell = None

    def __init__(self, func):
        """Initialize with `func` from which the ``%magic`` was created."""
        self.__func__ = func
        self.__module__ = func.__module__
        self.__name__ = func.__name__

    @abstractproperty
    def creator(self):  # pragma: no cover
        """
        Get the :class:`moreshell.IPython_magic` creator instance.

        The instance that was used as a decorator to create this ``%magic``

        Is abstract and must therefore be overridden in derived classes!
        """
        pass

    def load(self, shell):
        magics = shell.magics_manager.magics[self.kind_of_magic]
        magics[self.__name__] = self
        self.shell = shell

    def unload(self, shell):
        del shell.magics_manager.magics[self.kind_of_magic][self.__name__]
        self.shell = None

    def parse(self, line):
        """Parse the argument `line` of a ``%magic`` call."""
        return self.creator.parse_args(line.split())


class IPython_magic(zetup.program):
    """
    Decorator for turning a function into a new IPython ``%magic``.

    Based on and works just like the ``zetup.program`` decorator for
    simplifying the argument processing of functions used as
    ``entry_points`` for ``'console_scripts'``

    >>> from moreshell import IPython_magic, with_arguments

    >>> @IPython_magic(
    ...     with_arguments
    ...     ('value')
    ...     ('-f', '--flag')
    ...     ('-o', '--other-flag')
    ... )
    ... def new_magic(parsed_args):
    ...     do_something_with(parsed_args)

    >>> new_magic
    <%new_magic at ...>

    Now IPython offers a ``%new_magic`` supporting two option flags, which are
    automatically parsed with ``argparse.ArgumentParser.arg_parse`` before the
    actual ``new_magic`` function is called with the parsing result

    The resulting ``%new_magic`` object can be further used to create an
    accompanying cell magic:

    >>> @new_magic.cell_magic
    ... def new_magic(parsed_args, cell_block):
    ...     do_something_with(parsed_args)
    ...     and_with_the(cell_block)

    >>> new_magic.cell
    <%%new_magic at ...>

    For only creating a cell ``%%magic``,
    :class:`moreshell.IPython_cell_magic` must be used for initial decoration
    """

    __package__ = moreshell

    def __init__(self, arguments):
        """Prepare decorator with a :class:`zetup.with_arguments` object."""
        zetup.program.__init__(self, arguments)
        self.cell_magic = IPython_cell_magic(arguments)

    def parse_args(self, line):
        """
        Override ``argparse.ArgumentParser.parse_args``.

        Catch ``SystemExit`` and raise :exc:`moreshell.IPythonMagicExit`
        instead
        """
        try:
            return super(IPython_magic, self).parse_args(line)

        except SystemExit as exc:
            raise IPythonMagicExit(exc.code)

    def __call__(self, func, kind_of_magic='line'):
        """
        Decorate `func` to register as an IPython ``%magic``.

        The `kind_of_magic` parameter is only for internal use and creates a
        cell ``%%magic`` when changed to ``'cell'``
        """
        # to be used instead of self in the inner classes below
        magic_deco = self

        def cell_magic():
            """Create a cell ``%%magic`` instead of a line ``%magic``."""
            class cell_magic(magic_function):

                __module__ = None

                @property
                def creator(self):
                    return magic_deco

                def __call__(self, line, block):
                    return func(self.shell, self.parse(line), block)

            self.prog = '%%{}'.format(func.__name__)
            cell_magic.__name__ = cell_magic.__qualname__ = self.prog
            cell_magic.kind_of_magic = 'cell'
            return cell_magic(func)
            # magic = magics['cell'][func.__name__] = cell_magic(func)
            # return magic

        if kind_of_magic == 'line':
            class line_magic(magic_function):

                __module__ = None

                @property
                def creator(self):
                    return magic_deco

                def __call__(self, line):
                    return func(self.shell, self.parse(line))

                def cell_magic(self, func):
                    """Create an accompanying cell ``%%magic`` from `func`."""
                    self.cell = magic_deco.cell_magic(func)
                    return self

            self.prog = '%{}'.format(func.__name__)
            line_magic.__name__ = line_magic.__qualname__ = self.prog
            return line_magic(func)
            # magic = magics['line'][func.__name__] = line_magic(func)
            # return magic

        elif kind_of_magic == 'cell':
            return cell_magic()

        raise AssertionError(
            "kind_of_magic of {}.__call__ can be only two: 'line' or 'cell', "
            "not: {!r}".format(type(self), kind_of_magic))


class IPython_cell_magic(IPython_magic):
    """
    Decorator for turning a function into a new IPython cell ``%%magic``.

    >>> from moreshell import IPython_cell_magic, with_arguments

    >>> @IPython_cell_magic(
    ...     with_arguments
    ...     ('value')
    ...     ('-f', '--flag')
    ...     ('-o', '--other-flag')
    ... )
    ... def new_magic(parsed_args, cell_block):
    ...     do_something_with(parsed_args)
    ...     and_with_the(cell_block)

    >>> new_magic
    <%%new_magic at ...>
    """

    __package__ = moreshell

    def __init__(self, arguments):
        """Prepare decorator with a :class:`zetup.with_arguments` object."""
        zetup.program.__init__(self, arguments)

    def __call__(self, func):
        """Decorate `func` to register as an IPython cell ``%magic``."""
        self.prog = '%%{}'.format(func.__name__)
        return super(IPython_cell_magic, self).__call__(
            func, kind_of_magic='cell')
