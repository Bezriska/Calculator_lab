import pytest

from src.infix_to_postfix import tokenize, mark_unary, infix_to_postfix
from src.calculate import calculate_in_rpn
from src.errors import (
    DivisionByZeroError,
    InvalidOperatorError,
    NoOperatorBetweenNumbersError,
    TwooperatorsStraightError,
    NumAndBracketError,
    DoubleSlashTypeError,
    PercentTypeError,
)


def run_pipeline(expr):
    toks = tokenize(expr)
    marked = mark_unary(toks)
    rpn = infix_to_postfix(marked)
    return toks, marked, rpn, calculate_in_rpn(rpn)


# ----- Базовый функционал -----

def test_add_sub_mul_div():
    _, _, rpn, result = run_pipeline("2 + 3 * 4 - 6 / 3")
    assert rpn == ["2", "3", "4", "*", "+", "6", "3", "/", "-"]
    assert result == pytest.approx(2 + 3 * 4 - 6 / 3)


def test_power_and_explicit_pow():
    _, _, rpn1, res1 = run_pipeline("2 ^ 3")
    _, _, rpn2, res2 = run_pipeline("2 ** 3")
    assert rpn1 == ["2", "3", "^"]
    assert rpn2 == ["2", "3", "**"] or rpn2 == ["2", "3", "^"]
    assert res1 == pytest.approx(8.0)
    assert res2 == pytest.approx(8.0)


def test_integer_div_and_mod():
    _, _, rpn, result = run_pipeline("10 // 3")
    assert rpn == ["10", "3", "//"]
    assert result == pytest.approx(float(10 // 3))

    _, _, rpn2, result2 = run_pipeline("10 % 3")
    assert rpn2 == ["10", "3", "%"]
    assert result2 == pytest.approx(float(10 % 3))


def test_parentheses_and_precedence():
    _, _, rpn, result = run_pipeline("(2 + 3) * 4 ^ 2")
    assert rpn == ["2", "3", "+", "4", "2", "^", "*"]
    assert result == pytest.approx((2 + 3) * 4 ** 2)


# ----- Унарный минус -----

def test_unary_minus_simple():
    toks, marked, rpn, result = run_pipeline("-5 + 3")
    assert toks == ["-", "5", "+", "3"]
    assert "u-" in marked
    assert rpn[-1] == "+"
    assert result == pytest.approx(-2.0)


def test_unary_minus_inside_parens_and_double_unary():
    toks, marked, rpn, result = run_pipeline("2 * ( - -3 )")
    assert toks == ["2", "*", "(", "-", "-", "3", ")"]
    assert marked.count("u-") >= 1
    assert result == pytest.approx(6.0)


# ----- Ошибки и исключения -----

def test_division_by_zero_binary():
    toks = tokenize("10 / 0")
    marked = mark_unary(toks)
    rpn = infix_to_postfix(marked)
    with pytest.raises(DivisionByZeroError):
        calculate_in_rpn(rpn)


def test_double_slash_type_error_on_float():
    toks = tokenize("10.5 // 2")
    marked = mark_unary(toks)
    rpn = infix_to_postfix(marked)
    with pytest.raises(DoubleSlashTypeError):
        calculate_in_rpn(rpn)


def test_percent_type_error_on_float():
    toks = tokenize("10.5 % 2")
    marked = mark_unary(toks)
    rpn = infix_to_postfix(marked)
    with pytest.raises(PercentTypeError):
        calculate_in_rpn(rpn)


def test_invalid_operator_token_in_infix():
    toks = tokenize("5 $ 2")
    marked = mark_unary(toks)
    with pytest.raises(InvalidOperatorError):
        infix_to_postfix(marked)


def test_invalid_operator_in_rpn():
    with pytest.raises(InvalidOperatorError):
        calculate_in_rpn(["5", "2", "$"])


def test_no_operator_between_numbers_error():
    toks = tokenize("10 5 +")
    marked = mark_unary(toks)
    with pytest.raises(NoOperatorBetweenNumbersError):
        infix_to_postfix(marked)


def test_two_operators_straight_error():
    toks = tokenize("5 + * 2")
    marked = mark_unary(toks)
    with pytest.raises(TwooperatorsStraightError):
        infix_to_postfix(marked)


def test_mismatched_parentheses_error():
    toks = tokenize("(2 + 3")
    marked = mark_unary(toks)
    with pytest.raises(InvalidOperatorError):
        infix_to_postfix(marked)


# ----- Граничные случаи -----

def test_empty_expression():
    toks = tokenize("")
    marked = mark_unary(toks)
    with pytest.raises(ValueError):
        infix_to_postfix(marked)


def test_extra_operands_in_rpn_detected():
    with pytest.raises(ValueError):
        calculate_in_rpn(["2", "3", "4", "+"])