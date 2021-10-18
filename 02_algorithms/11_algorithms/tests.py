import math
import pytest
from algorithms import binary_search, quick_sort_iterative, my_factorial


def test_binary_sorted():
    """ test for binary search """
    with pytest.raises(ValueError):
        assert binary_search([1, 3, 2, 6, 5], 2)


def test_binary_correct_numbers():
    """ Simple binary test for check different values cases """
    data = [1, 3, 4, 5, 6, 8, 9, 15, 26]
    assert binary_search(data, 1) == 0, "Wrong 1st item index"
    assert binary_search(data, 2) == -1, "Wrong not found index"
    assert binary_search(data, -2) == -1, "Wrong not found index"
    assert binary_search(data, 12) == -1, "Wrong not found index"
    assert binary_search(data, 26) == 8, "Wrong 1st item index"


def test_binary_correct_letters():
    """ The same binary test but with letters """
    data = ["a", "b", "c", "d", "e", "f", "g", "h"]
    assert binary_search(data, "h") == 7, "Wrong 8th letter element index"
    assert binary_search(data, "z") == -1, "Wrong not found letter"
    assert binary_search(data, "H") == -1, "Wrong not found letter"


@pytest.mark.parametrize("list", [[-1, 1, 2,  4, -2, 9, 12, 4, 42, 24],
                                  ["a", "b", "e", "z", "A"],
                                  [7.8, 2, 1, -2.4, 8.5, 6, 3, 5, 4.2, 4.6, 20, -34, 42],
                                  [2, 5, 9, 1, 5, 0, 2, 1, 4,5, 10, 5]])
def test_quick_sort_numbers(list):
    """ Check is quick sorting implementation works fine """
    assert quick_sort_iterative(list) == sorted(list), "Wrong sorting result!"


@pytest.mark.parametrize("input", [1, 5, 2, 10, 0])
def test_factorial(input):
    """ Factorial test """
    assert my_factorial(input) == math.factorial(input), "Error in factorial function. Wrong result."


@pytest.mark.parametrize("input", [-5])
def test_factorial_negative(input):
    """ Factorial must raise an error if not positive number was given """
    with pytest.raises(ValueError):
        assert my_factorial(input) == math.factorial(input), "Error in factorial function. Wrong result."

