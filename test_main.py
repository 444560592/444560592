"""
Unit tests for main.py calculator functions.
"""

import pytest
from main import add, subtract, multiply, divide


def test_add():
    assert add(3, 4) == 7
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(1.5, 2.5) == 4.0


def test_subtract():
    assert subtract(10, 3) == 7
    assert subtract(0, 5) == -5
    assert subtract(-2, -3) == 1
    assert subtract(2.5, 1.0) == 1.5


def test_multiply():
    assert multiply(6, 7) == 42
    assert multiply(0, 100) == 0
    assert multiply(-3, 4) == -12
    assert multiply(1.5, 2) == 3.0


def test_divide():
    assert divide(9, 3) == 3.0
    assert divide(10, 4) == 2.5
    assert divide(-6, 2) == -3.0
    assert divide(0, 5) == 0.0


def test_divide_by_zero():
    with pytest.raises(ValueError, match="除数不能为零"):
        divide(5, 0)
