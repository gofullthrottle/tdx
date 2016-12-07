import copy

import pytest

from ..collections import (
    get_by_specifier,
    add_dicts,
    add_sets,
    add_lists,
    flatten,
)


def test_add_dicts_works():

    msg = "works for a single empty dict"
    dicts = [{}]
    expected = {}
    actual = add_dicts(*dicts)
    assert actual == expected, msg

    msg = "works for several empty dicts"
    dicts = [{}, {}, {}]
    expected = {}
    actual = add_dicts(*dicts)
    assert actual == expected, msg

    msg = "works for a single nonempty dict"
    dicts = [{'a': 1, 'b': 2}]
    expected = {'a': 1, 'b': 2}
    actual = add_dicts(*dicts)
    assert actual == expected, msg

    msg = "works for a several nonempty dicts"
    dicts = [{'a': 1, 'b': 2}, {'c': 3}, {'d': 4}]
    expected = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    actual = add_dicts(*dicts)
    assert actual == expected, msg

    msg = "does not modify inputs"
    dicts = [{'a': 1, 'b': 2}, {'c': 3}, {'d': 4}]
    dicts_copy = copy.deepcopy(dicts)
    expected = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    add_dicts(*dicts)
    assert dicts == dicts_copy, msg


def test_add_dicts_raises_on_duplicate_keys():
    dicts = [{'a': 1, 'b': 2}, {'a': 3}, {'d': 4}]
    with pytest.raises(ValueError):
        add_dicts(*dicts)


def test_add_sets():

    msg = "works for a single empty set"
    args = [set()]
    expected = set()
    actual = add_sets(*args)
    assert actual == expected, msg

    msg = "works for a simple set"
    args = [{"a", "b"}]
    expected = {"a", "b"}
    actual = add_sets(*args)
    assert actual == expected, msg

    msg = "works for a simple list"
    args = [["a", "b"]]
    expected = {"a", "b"}
    actual = add_sets(*args)
    assert actual == expected, msg

    msg = "works for a simple dict (uses keys)"
    args = [{"a": 1, "b": 2}]
    expected = {"a", "b"}
    actual = add_sets(*args)
    assert actual == expected, msg

    msg = "works for several sets"
    args = [{"a", "b"}, {"c"}, set()]
    expected = {"a", "b", "c"}
    actual = add_sets(*args)
    assert actual == expected, msg


def test_add_lists():

    msg = "works for a single empty list"
    args = [[]]
    expected = []
    actual = add_lists(*args)
    assert actual == expected, msg

    msg = "works for a simple list"
    args = [["a", "b"]]
    expected = ["a", "b"]
    actual = add_lists(*args)
    assert actual == expected, msg

    msg = "works for several lists"
    args = [["a", "b"], ["c", "d"]]
    expected = ["a", "b", "c", "d"]
    actual = add_lists(*args)
    assert actual == expected, msg


def test_flatten():

    # The first three tests are identical to add_lists tests.

    msg = "works for a single empty list"
    args = [[]]
    expected = []
    actual = list(flatten(*args))
    assert actual == expected, msg

    msg = "works for a simple list"
    args = [["a", "b"]]
    expected = ["a", "b"]
    actual = list(flatten(*args))
    assert actual == expected, msg

    msg = "works for several lists"
    args = [["a", "b"], ["c", "d"]]
    expected = ["a", "b", "c", "d"]
    actual = list(flatten(*args))
    assert actual == expected, msg

    # the last test is verifying that flatten is lazy
    args = [(8 for i in range(3)), (i/0 for i in [1, 2])]
    flattened = flatten(*args)  # the key is that this doens't raise
    with pytest.raises(ZeroDivisionError):
        list(flattened)


def test_get_by_specifier_raises():
    # invalid specifier
    with pytest.raises(ValueError):
        get_by_specifier('a..', {})
    # invalid dict key
    with pytest.raises(KeyError):
        get_by_specifier('a', {})
    # invalid list index
    with pytest.raises(IndexError):
        get_by_specifier('[0]', [])


def test_get_by_specifier_works():
    def run_test_case(specifier, collection, expected, description):
        actual = get_by_specifier(specifier, collection)
        assert actual == expected, description

    test_cases = [
        {'specifier': '[0]',
         'collection': ['a', 'b'],
         'expected': 'a',
         'description': 'basic list indexing'},
        {'specifier': 'k',
         'collection': {'k': 'v'},
         'expected': 'v',
         'description': 'basic dict indexing'},
        {'specifier': 'k',
         'collection': {'k': 'v'},
         'expected': 'v',
         'description': 'list + dict indexing'},
        {'specifier': '[0].k',
         'collection': [{'k': 'v'}],
         'expected': 'v',
         'description': 'list + dict indexing'},
        {'specifier': 'k[0][1]',
         'collection': {'k': [['a', 'v']]},
         'expected': 'v',
         'description': 'dict + list indexing'},
        {'specifier': 'k.k1',
         'collection': {'k': {'k0': 'a', 'k1': 'b'}},
         'expected': 'b',
         'description': 'nested dict indexing'},
    ]
    for test_case in test_cases:
        run_test_case(**test_case)
