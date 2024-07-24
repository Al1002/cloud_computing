from context import app
import pytest

import app.special.test as test


def test_add_two_nums():
    assert test.add_two_nums(1,2) == 3
    assert test.add_two_nums(6,-8.5) == -2.5
    with pytest.raises(Exception) as ex: # assert an exception is raised
        assert test.add_two_nums(1,2) == 4
    with pytest.raises(Exception) as ex:
        test.add_two_nums("Helo", None)