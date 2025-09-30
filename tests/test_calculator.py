import pytest
from src.infix_to_postfix import tokenize, mark_unary, infix_to_postfix
from src.calculate import calculate_in_rpn
from src.errors import (
    NumAndBracketError,
    NoOperatorBetweenNumbersError,
    DoubleSlashTypeError,
    PercentTypeError,
    DivisionByZeroError,
    InvalidOperatorError,
)


def run_pipeline(expr):
    toks = tokenize(expr)
    marked = mark_unary(toks)
    rpn = infix_to_postfix(marked)
    return toks, marked, rpn, calculate_in_rpn(rpn)


def test_unary_minus_simple():
    toks, marked, rpn, result = run_pipeline("-5 + 3")
    assert toks == ["-", "5", "+", "3"]
    assert marked == ["u-", "5", "+", "3"]
    assert rpn == ["5", "u-", "3", "+"]
    assert result == -2.0


def test_unary_minus_after_open_paren():
    toks, marked, rpn, result = run_pipeline("2 * ( -3 )")
    assert toks == ["2", "*", "(", "-", "3", ")"]
    assert marked == ["2", "*", "(", "u-", "3", ")"]
    assert rpn == ["2", "3", "u-", "*"]
    assert result == -6.0


def test_num_and_open_bracket_error():
    with pytest.raises(NumAndBracketError):
        tokenize("5(")
        marked = mark_unary(tokenize("5("))
        infix_to_postfix(marked)


def test_no_operator_between_numbers_error():
    with pytest.raises(NoOperatorBetweenNumbersError):
        toks = tokenize("10 5 +")
        marked = mark_unary(toks)
        infix_to_postfix(marked)


# ---- Базовые бинарные операторы ----


def test_add_sub_mul_div():
    _, _, rpn, result = run_pipeline("2 + 3 * 4 - 6 / 3")
    assert rpn == ["2", "3", "4", "*", "+", "6", "3", "/", "-"]
    assert result == pytest.approx(2 + 3 * 4 - 6 / 3)


def test_power_and_explicit_pow():
    # '^' и '**' оба поддерживаются и работают одинаково
    _, _, rpn1, res1 = run_pipeline("2 ^ 3")
    _, _, rpn2, res2 = run_pipeline("2 ** 3")
    assert rpn1 == ["2", "3", "^"]
    assert rpn2 == ["2", "3", "**"]
    assert res1 == pytest.approx(8.0)
    assert res2 == pytest.approx(8.0)


def test_precedence_and_parentheses():
    # скобки имеют приоритет
    _, _, rpn, result = run_pipeline(" ( 2 + 3 ) * 4 ^ 2 ")
    assert rpn == ["2", "3", "+", "4", "2", "^", "*"]
    assert result == pytest.approx((2 + 3) * 4**2)


# ---- Целочисленные операции // и % ----


def test_double_slash_integer_ok():
    _, _, rpn, result = run_pipeline("10 // 3")
    assert rpn == ["10", "3", "//"]
    assert result == pytest.approx(float(10 // 3))


def test_percent_integer_ok():
    _, _, rpn, result = run_pipeline("10 % 3")
    assert rpn == ["10", "3", "%"]
    assert result == pytest.approx(float(10 % 3))


def test_double_slash_type_error_on_float():
    toks = tokenize("10.5 // 2")
    marked = mark_unary(toks)
    with pytest.raises(DoubleSlashTypeError) as exc:
        rpn = infix_to_postfix(marked)
        # если infix_to_postfix не выбросил, вызываем вычисление
        calculate_in_rpn(infix_to_postfix(marked))
    # либо проверяем при вычислении типа исключения:
    # повторно выполнить pipeline и поймать на calculate_in_rpn
    toks2 = tokenize("10.5 // 2")
    marked2 = mark_unary(toks2)
    rpn2 = infix_to_postfix(marked2)
    with pytest.raises(DoubleSlashTypeError):
        calculate_in_rpn(rpn2)


def test_percent_type_error_on_float():
    toks = tokenize("10.5 % 2")
    marked = mark_unary(toks)
    rpn = infix_to_postfix(marked)
    with pytest.raises(PercentTypeError):
        calculate_in_rpn(rpn)


# ---- Деление на ноль ----


def test_division_by_zero_binary():
    toks = tokenize("10 / 0")
    marked = mark_unary(toks)
    rpn = infix_to_postfix(marked)
    with pytest.raises(DivisionByZeroError):
        calculate_in_rpn(rpn)


def test_double_slash_division_by_zero():
    toks = tokenize("10 // 0")
    marked = mark_unary(toks)
    rpn = infix_to_postfix(marked)
    with pytest.raises(DivisionByZeroError):
        calculate_in_rpn(rpn)


def test_modulo_division_by_zero():
    toks = tokenize("10 % 0")
    marked = mark_unary(toks)
    rpn = infix_to_postfix(marked)
    with pytest.raises(DivisionByZeroError):
        calculate_in_rpn(rpn)


# ---- Некорректные операторы ----


def test_invalid_operator_token():
    toks = tokenize("5 $ 2")
    marked = mark_unary(toks)
    with pytest.raises(InvalidOperatorError):
        infix_to_postfix(marked)


def test_invalid_operator_in_rpn():
    # вручную создаём некорректный RPN, чтобы проверить поведение calculate
    with pytest.raises(InvalidOperatorError):
        calculate_in_rpn(["5", "2", "$"])
