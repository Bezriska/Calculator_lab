from src.precedence import precedence
from src.errors import (
    InvalidOperatorError,
    NoOperatorBetweenNumbersError,
    TwooperatorsStraightError,
    NumAndBracketError,
)
from src.is_number import is_number
from src.check_operators import check_operators
from src.check_operators import check_numbers
from src.check_operators import check_open_bracket


def tokenize(expr: str) -> list[str]:
    """Токенизирует строку выражения в список токенов

    Args:
        expr (str): входное выражение

    Raises:
        ValueError: ошибка недопустимого оператора

    Returns:
        list[str]: список токенов
    """
    tokens = []
    i = 0
    n = len(expr)

    def peek(offset=0):
        return expr[i + offset] if i + offset < n else ""

    while i < n:
        ch = expr[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit() or (ch == "." and peek(1).isdigit()):
            start = i
            while i < n and expr[i].isdigit():
                i += 1
            if i < n and expr[i] == ".":
                i += 1
                while i < n and expr[i].isdigit():
                    i += 1
            tokens.append(expr[start:i])
            continue

        if ch == "/" and peek(1) == "/":
            tokens.append("//")
            i += 2
            continue

        if ch in "+-*/^%()":
            tokens.append(ch)
            i += 1
            continue

        raise ValueError(f"Недопустимый оператор: {ch}")

    return tokens


def mark_unary(tokens: list[str]) -> list[str]:
    """Помечает унарный минус в списке токенов

    Args:
        tokens (list[str]): список токенов

    Returns:
        list[str]: список токенов с помеченным унарным минусом
    """
    mark_unary_result = []
    prev = None
    for token in tokens:
        if token in ("+", "-") and (
            prev is None or prev in ("(", "+", "-", "*", "/", "//", "^", "%")
        ):
            if token == "-":
                mark_unary_result.append("u-")
        else:
            mark_unary_result.append(token)
        prev = token
    return mark_unary_result


def infix_to_postfix(mark_unary_result) -> list:
    """Переводит инфиксное выражение в постфиксное

    Args:
        expression (str): инфиксное выражение

    Raises:
        NoOperatorBetweenNumbersError: проверяет, что между двумя числами есть оператор.
        TwooperatorsStraightError: проверяет, что между двумя операторами есть число.
        NumAndBracketError: проверяет, что между числом и открывающей\закрывающей скобками есть оператор.
        InvalidOperatorError: проверяет, что оператор допустим

    Returns:
        list: преобразованное постфиксное выражение
    """
    output = []
    stack = []

    if not mark_unary_result:
        raise ValueError("Пустое выражение")

    if len(mark_unary_result) == 1 and is_number(mark_unary_result[0]):
        raise ValueError("Выражение должно содержать оператор")

    if not check_operators(mark_unary_result):
        raise NoOperatorBetweenNumbersError(
            f"Ошибка: отсутствует оператор между числами"
        )

    if not check_numbers(mark_unary_result):
        raise TwooperatorsStraightError(f"Oшибка: два оператора идут подряд")

    if not check_open_bracket(mark_unary_result):
        raise NumAndBracketError(
            f"Oшибка: число и открывающая/закрывающая скобка идут подряд"
        )

    for token in mark_unary_result:

        is_right_assoc = token in ("^", "u-")

        if token not in (
            "+",
            "-",
            "*",
            "/",
            "^",
            "(",
            ")",
            "u-",
            "//",
            "%",
        ) and not is_number(token):
            raise InvalidOperatorError(f"Недопустимый оператор: {token}")

        if is_number(token):
            output.append(token)
            continue

        if token == "(":
            stack.append(token)
            continue

        if token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise InvalidOperatorError("Несовпадающие скобки")
            stack.pop()
            continue

        while stack and stack[-1] != "(":
            top = stack[-1]
            if (
                not is_right_assoc
                and precedence(top) >= precedence(token)
                or is_right_assoc
                and precedence(top) > precedence(token)
            ):
                output.append(stack.pop())
            else:
                break
        stack.append(token)

    while stack:
        top = stack.pop()
        if top in ("(", ")"):
            raise InvalidOperatorError("Несовпадающие скобки")
        output.append(top)

    return output
