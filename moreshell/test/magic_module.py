import sys

from path import Path
from zetup import call

import moreshell
from moreshell import IPython_magic_module, with_arguments

IPython_magic, IPython_cell_magic = IPython_magic_module(__name__, [
    'test_moreshell',
])


@IPython_magic(
    with_arguments
    ('--coverage', action='store_true')
    ('--verbose', action='store_true')
)
def test_moreshell(shell, args):  # pragma: no cover
    """Run the :mod:`moreshell` unit tests with ``pytest``."""
    moreshell_dir = Path(  # pylint: disable=no-value-for-parameter
        moreshell.__file__
    ).dirname().realpath()

    call_args = [
        sys.executable, '-m', 'pytest', moreshell_dir]
    if args.coverage:
        call_args.extend([
            '--cov', moreshell_dir, '--cov-report', 'term-missing'])
    if args.verbose:
        call_args.append('-vv')

    call(call_args)
