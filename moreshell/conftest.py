import pytest


@pytest.fixture
def magic_module__name__():
    return '.'.join((__package__, 'test', 'magic_module'))


@pytest.fixture
def shell():
    class shell_mock(object):
        class magics_manager(object):
            magics = {'line': {}, 'cell': {}}
    return shell_mock
