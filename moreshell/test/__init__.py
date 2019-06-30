"""A package for testing moreshell in IPython via ``%load_ext``."""


def load_ipython_extension(shell):  # pragma: no cover
    """Provide the handler for ``%load_ext moreshell.test`` in IPython."""
    from moreshell import load_magic_modules

    load_magic_modules('magic_module', package=__name__, shell=shell)
