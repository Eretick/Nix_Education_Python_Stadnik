import math
import string
import pytest
from algorithms import binary_search, quick_sort_iterative, my_factorial
import random

def test_binary_not_sorted():
    """ test for binary search if list is not sorted"""
    with pytest.raises(ValueError):
        not_full = list([i for i in range(0, 5)])
        not_full.pop(2)
        assert binary_search(not_full, 2)


def test_binary_correct_numbers():
    """ Simple binary test for check different values cases """
    data = sorted([random.randint(0, 20) for i in range(9)])
    numbers = [random.randint(-2, 10) for i in range(9)]
    for i in numbers:
        if i in data:
            assert binary_search(data, i) == data.index(i), f"Wrong index of {i}"
        else:
            with pytest.raises(ValueError):
                assert binary_search(data, i) == data.index(i), "Wrong not found index"


def test_binary_correct_letters():
    """ The same binary test but with letters """
    letters_list = [i for i in sorted(string.ascii_letters)][0:-5]
    assert binary_search(letters_list, "h") == letters_list.index("h"), "Wrong 8th letter element index"
    with pytest.raises(ValueError):
        assert binary_search(letters_list, "z"), "Must be a value error if search element not in list"
    assert binary_search(letters_list, "A") == letters_list.index("A")


@pytest.mark.parametrize("list", [[random.randint(-50, 50) for i in range(20)],
                                  [i for i in string.ascii_letters],
                                  [random.uniform(0, 50) for i in range(7)],
                                  ])
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

