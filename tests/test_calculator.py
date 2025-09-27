from src.infix_to_postfix import infix_to_postfix
from src.clculate import calculate_in_rpn
import pytest


def test_base_func():
    expr = "2 ^ 6 + 10 - 5 * ( 10 // 2 ) + 2 % 5"
    postfix = infix_to_postfix(expr)
    assert postfix == [
        "2",
        "4",
        "6",
        "2",
        "5",
        "^",
        "5",
        "//",
        "7",
        "%",
        "*",
        "+",
        "10",
        "2",
        "/",
        "-",
    ]
    result = calculate_in_rpn(postfix)
    assert result == 51.0
