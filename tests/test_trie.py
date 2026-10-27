import pytest

from autocomplete.trie import Trie


def make_trie() -> Trie:
    trie = Trie()
    trie.insert_word("apple", 2.0)
    trie.insert_word("application", 3.0)
    trie.insert_word("apply", 1.0)
    trie.insert_word("banana", 0.5)
    return trie


def test_autocomplete_returns_prefix_matches_by_score():
    trie = make_trie()
    assert trie.autocomplete("app") == [
        ("apply", 1.0),
        ("apple", 2.0),
        ("application", 3.0),
    ]


def test_missing_prefix_returns_empty_list():
    assert make_trie().autocomplete("xyz") == []


def test_top_n_limits_results():
    assert make_trie().autocomplete("app", top_n=2) == [
        ("apply", 1.0),
        ("apple", 2.0),
    ]


def test_equal_scores_are_sorted_alphabetically():
    trie = Trie()
    trie.insert_word("car", 1.0)
    trie.insert_word("cat", 1.0)
    assert trie.autocomplete("ca") == [("car", 1.0), ("cat", 1.0)]


def test_duplicate_word_updates_score():
    trie = Trie()
    trie.insert_word("hello", 4.0)
    trie.insert_word("hello", 1.0)
    assert trie.autocomplete("he") == [("hello", 1.0)]


def test_empty_word_is_rejected():
    with pytest.raises(ValueError):
        Trie().insert_word("")


def test_non_positive_top_n_returns_empty_list():
    assert make_trie().autocomplete("app", top_n=0) == []
