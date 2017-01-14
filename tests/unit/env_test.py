import pytest

from examples import environment_name2value


parametrize = pytest.mark.parametrize


@parametrize('env, name, result', environment_name2value)
def test_lookup(env, name, result):
    assert env.lookup(name) == result
