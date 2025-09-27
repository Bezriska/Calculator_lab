import pytest
from src.infix_to_postfix import infix_to_postfix
from src.clculate import calculate_in_rpn
from src.errors import (
    InvalidOperatorError,
    DivisionByZeroError,
    PercentTypeError,
    DoubleSlashTypeError,
    NoOperatorBetweenNumbersError,
    TwooperatorsStraightError,
    NumAndBracketError,
)


def test_division_by_zero():
    expr = "10 / 0"
    postfix = infix_to_postfix(expr)
    assert postfix == ["10", "0", "/"]
    try:
        calculate_in_rpn(postfix)
    except DivisionByZeroError as e:
        assert str(e) == "Ошибка: Деление на 0"


def test_invalid_operator():
    expr = "10 $ 2"
    postfix = infix_to_postfix(expr)
    assert postfix == ["10", "2", "$"]
    try:
        calculate_in_rpn(postfix)
    except InvalidOperatorError as e:
        assert str(e) == f"Ошибка: Недопустимый оператор {e.operator}"


def test_percent_type_error():
    expr = "10.3 % 7"
    postfix = infix_to_postfix(expr)
    assert postfix == ["10.3", "7", "%"]
    try:
        calculate_in_rpn(postfix)
    except PercentTypeError as e:
        assert (
            str(e)
            == f"Ошибка: операция % не поддерживается для типа {e.type_}, используйте только целые числа"
        )


def test_double_slash_type_error():
    expr = "10.3 // 7"
    postfix = infix_to_postfix(expr)
    assert postfix == ["10.3", "7", "//"]
    try:
        calculate_in_rpn(postfix)
    except DoubleSlashTypeError as e:
        assert (
            str(e)
            == f"Ошибка: операция // не поддерживается для типа {e.type_}, используйте только целые числа"
        )


def test_no_operator_between_numbers():
    expr = "10 5 + 2"
    try:
        infix_to_postfix(expr)
    except NoOperatorBetweenNumbersError:
        assert True
    else:
        assert False, "Expected NoOperatorBetweenNumbersError"


def test_two_operators_straight():
    expr = "10 + * 2"
    try:
        infix_to_postfix(expr)
    except TwooperatorsStraightError:
        assert True
    else:
        assert False, "Expected TwooperatorsStraightError"


def tets_num_and_bracket():
    expr = "10 ( 5 + 2 )"
    try:
        infix_to_postfix(expr)
    except NumAndBracketError:
        assert True
    else:
        assert False, "Expected NumAndBracketError"
