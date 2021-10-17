import pytest
from algorithms import binary


def test_sorted_binary():
    with pytest.raises(ValueError):
        assert binary([1,3,2,6,5], 2)


def test_correct_numbers():
    data = [1, 3, 4, 5, 6, 8, 9, 15, 26]
    assert binary(data, 1) == 0, "Wrong 1st item index"
    assert binary(data, 2) == -1, "Wrong not found index"
    assert binary(data, -2) == -1, "Wrong not found index"
    assert binary(data, 12) == -1, "Wrong not found index"
    assert binary(data, 26) == 8, "Wrong 1st item index"


def test_correct_letters():
    data = ["a", "b", "c", "d", "e", "f", "g", "h"]
    assert binary(data, "h") == 7, "Wrong 8th letter element index"
    assert binary(data, "z") == -1, "Wrong not found letter"
    assert binary(data, "H") == -1, "Wrong not found letter"

