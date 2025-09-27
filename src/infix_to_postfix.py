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


def infix_to_postfix(expression):
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
    tokens = expression.split()
    prev_token = None

    for token in tokens:
        if token == "-" and (
            prev_token is None
            or prev_token in ("(", "+", "-", "*", "/", "^", "//", "%")
        ):
            stack.append("u-")

        elif token == "+" and (
            prev_token is None
            or prev_token in ("(", "+", "-", "*", "/", "^", "//", "%")
        ):
            continue

        elif check_operators(tokens) == False:
            raise NoOperatorBetweenNumbersError()

        elif check_numbers(tokens) == False:
            raise TwooperatorsStraightError()

        elif check_open_bracket(tokens) == False:
            raise NumAndBracketError()

        elif token not in (
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
            raise InvalidOperatorError(token)

        elif is_number(token):
            output.append(token)

        elif token == "(":
            stack.append(token)

        elif token == ")":
            # выталкиваем до открывающей скобки
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()  # убираем "(" из стека

        else:
            # выталкиваем более приоритетные
            while stack and precedence(stack[-1]) >= precedence(token):
                output.append(stack.pop())
            stack.append(token)
        prev_token = token

    # выталкиваем оставшиеся операторы
    while stack:
        output.append(stack.pop())

    return output
