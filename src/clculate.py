from src.errors import (
    InvalidOperatorError,
    DivisionByZeroError,
    DoubleSlashTypeError,
    PercentTypeError,
)
from src.is_number import is_number


def calculate_in_rpn(lst_rpn):
    """Считает значение выражения в обратной польской записи

    Args:
        lst_rpn (list): список токенов в обратной польской записи

    Raises:
        DivisionByZeroError: проверяет деление на ноль
        DoubleSlashTypeError: проверяет, что операнды для // целые числа
        DivisionByZeroError: проверяет деление нацело на ноль
        PercentTypeError: проверяет, что операнды для % целые числа
        DivisionByZeroError: проверяет деление с остатком на ноль
        InvalidOperatorError: проверяет, что оператор допустим

    Returns:
        float: ответ выражения
    """
    stack = []
    for token in lst_rpn:
        if token == "u-":
            a = stack.pop()
            stack.append(-a)

        elif is_number(token):
            stack.append(float(token))

        elif token in ("+", "-", "*", "/", "^", "//", "%"):
            b = stack.pop()
            a = stack.pop()

            if token == "+":
                stack.append(a + b)

            elif token == "-":
                stack.append(a - b)

            elif token == "*":
                stack.append(a * b)

            elif token == "/":
                if b == 0:
                    raise DivisionByZeroError()
                stack.append(a / b)

            elif token == "^":
                stack.append(a**b)

            elif token == "//":
                if not (a.is_integer() and b.is_integer()):
                    raise DoubleSlashTypeError(
                        "Операция // поддерживается только для целых чисел"
                    )
                if b == 0:
                    raise DivisionByZeroError()
                stack.append(float(int(a) // int(b)))
            elif token == "%":
                if not (a.is_integer() and b.is_integer()):
                    raise PercentTypeError(
                        "Операция % поддерживается только для целых чисел"
                    )
                if b == 0:
                    raise DivisionByZeroError()
                stack.append(float(int(a) % int(b)))
        else:
            raise InvalidOperatorError(token)

    return stack[0]
