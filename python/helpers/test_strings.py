import pytest

from python.helpers.strings import truncate_text


def test_truncate_text_end_respects_length():
    text = "abcdefghijklmnopqrstuvwxyz"
    result = truncate_text(text, 10)
    assert result == "abcdefg..."
    assert len(result) == 10


def test_truncate_text_start_respects_length():
    text = "abcdefghijklmnopqrstuvwxyz"
    result = truncate_text(text, 10, at_end=False)
    assert result == "...tuvwxyz"
    assert len(result) == 10


def test_truncate_text_replacement_longer_than_length():
    text = "hello"
    result = truncate_text(text, 2)
    assert result == ".."
