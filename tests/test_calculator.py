import pytest

from src.calculator import (
    calculate_average,
    find_maximum,
    is_prime,
    factorial,
    power,
)


# =====================================================
# calculate_average
# =====================================================

@pytest.mark.parametrize("scores, expected", [
    ([80, 90, 100], 90.0),      # normal list
    ([50], 50.0),               # only one score
    ([0], 0.0),                 # lowest allowed score
    ([100], 100.0),             # highest allowed score
    ([0, 100], 50.0),           # both edges together
    ([85.5, 90.5], 88.0),       # float scores
    ([90, 85, 80.5], 85.17),    # needs rounding
])
def test_average_valid(scores, expected):
    assert calculate_average(scores) == expected


def test_average_works_with_tuple():
    assert calculate_average((60, 80)) == 70.0


def test_average_rounds_to_2_decimals():
    # 31 / 3 = 10.3333..., so the answer should be 10.33
    assert calculate_average([10, 10, 11]) == 10.33


@pytest.mark.parametrize("scores", [[], ()])
def test_average_empty_raises_value_error(scores):
    with pytest.raises(ValueError, match="empty"):
        calculate_average(scores)


@pytest.mark.parametrize("scores", [
    [-1],
    [-0.01],        # just below 0
    [100.01],       # just above 100
    [101],
    [50, 101],      # bad score is not the first one
    [50, 50, -1],   # bad score is the last one
])
def test_average_out_of_range_raises_value_error(scores):
    with pytest.raises(ValueError, match="out of valid bounds"):
        calculate_average(scores)


@pytest.mark.parametrize("scores", ["80,90", 80, None, {80, 90}, 50.5])
def test_average_not_a_list_raises_type_error(scores):
    with pytest.raises(TypeError):
        calculate_average(scores)


@pytest.mark.parametrize("scores", [
    ["90"],         # text
    [None],         # nothing
    [80, "a"],      # one bad item in the middle of good ones
    [True],         # booleans are not allowed
    [80, False],
])
def test_average_bad_item_raises_type_error(scores):
    with pytest.raises(TypeError):
        calculate_average(scores)


# =====================================================
# find_maximum
# =====================================================

@pytest.mark.parametrize("numbers, expected", [
    ([1, 2, 3], 3),             # biggest at the end
    ([3, 2, 1], 3),             # biggest at the start
    ([2, 9, 4], 9),             # biggest in the middle
    ([-5, -1, -10], -1),        # all negative
    ([-3, 0, 4], 4),            # mixed
    ([7], 7),                   # one item
    ([5, 5, 5], 5),             # all the same
    ([1, 9, 9, 2], 9),          # biggest appears twice
    ([1.5, 2.5, 0.5], 2.5),     # floats
    ([3, 3.5], 3.5),            # int and float together
])
def test_maximum_valid(numbers, expected):
    assert find_maximum(numbers) == expected


def test_maximum_works_with_tuple():
    assert find_maximum((4, 8, 6)) == 8


@pytest.mark.parametrize("numbers", [[], ()])
def test_maximum_empty_raises_value_error(numbers):
    with pytest.raises(ValueError, match="empty"):
        find_maximum(numbers)


@pytest.mark.parametrize("numbers", ["123", 5, None, {1, 2, 3}])
def test_maximum_not_a_list_raises_type_error(numbers):
    with pytest.raises(TypeError):
        find_maximum(numbers)


@pytest.mark.parametrize("numbers", [
    ["a"],
    [1, "2"],
    [1, None, 3],
    [True],
    [1, True],
])
def test_maximum_bad_item_raises_type_error(numbers):
    with pytest.raises(TypeError):
        find_maximum(numbers)


# =====================================================
# is_prime
# =====================================================

@pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 29, 97, 101, 7919])
def test_is_prime_true(n):
    assert is_prime(n) is True


@pytest.mark.parametrize("n", [-100, -7, -1, 0, 1])
def test_is_prime_zero_one_and_negatives_are_false(n):
    assert is_prime(n) is False


@pytest.mark.parametrize("n", [4, 6, 8, 10, 100])
def test_is_prime_even_numbers_are_false(n):
    assert is_prime(n) is False


@pytest.mark.parametrize("n", [9, 15, 21, 25, 35, 49, 77, 91, 121, 169, 7921])
def test_is_prime_odd_non_primes_are_false(n):
    assert is_prime(n) is False


@pytest.mark.parametrize("n", [2.0, 7.5, "7", None, True, False])
def test_is_prime_bad_type_raises_type_error(n):
    with pytest.raises(TypeError, match="integer"):
        is_prime(n)


# =====================================================
# factorial
# =====================================================

@pytest.mark.parametrize("n, expected", [
    (0, 1),                         # 0! is 1
    (1, 1),
    (2, 2),
    (3, 6),
    (5, 120),
    (10, 3628800),
    (20, 2432902008176640000),      # big number
])
def test_factorial_valid(n, expected):
    assert factorial(n) == expected


@pytest.mark.parametrize("n", [-1, -5, -100])
def test_factorial_negative_raises_value_error(n):
    with pytest.raises(ValueError, match="negative"):
        factorial(n)


@pytest.mark.parametrize("n", [3.0, 2.5, "3", None, True, False])
def test_factorial_bad_type_raises_type_error(n):
    with pytest.raises(TypeError, match="integer"):
        factorial(n)


# =====================================================
# power
# =====================================================

@pytest.mark.parametrize("base, exponent, expected", [
    (2, 3, 8),              # normal
    (2, 10, 1024),
    (5, 1, 5),
    (5, 0, 1),              # anything to the power 0 is 1
    (-3, 0, 1),
    (0, 0, 1),
    (0, 5, 0),              # zero to a positive power
    (-2, 3, -8),            # negative base, odd power
    (-2, 2, 4),             # negative base, even power
    (2, -1, 0.5),           # negative exponent
    (2, -2, 0.25),
    (10, -1, 0.1),
    (2.5, 2, 6.25),         # float base
])
def test_power_valid(base, exponent, expected):
    assert power(base, exponent) == expected


@pytest.mark.parametrize("base, exponent", [(0, -1), (0, -5), (0.0, -2)])
def test_power_zero_to_negative_raises_value_error(base, exponent):
    with pytest.raises(ValueError, match="zero"):
        power(base, exponent)


@pytest.mark.parametrize("base", ["2", None, True, False])
def test_power_bad_base_raises_type_error(base):
    with pytest.raises(TypeError, match="Base"):
        power(base, 2)


@pytest.mark.parametrize("exponent", [2.0, 0.5, "2", None, True, False])
def test_power_bad_exponent_raises_type_error(exponent):
    with pytest.raises(TypeError, match="Exponent"):
        power(2, exponent)