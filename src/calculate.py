from src.errors import (
    InvalidOperatorError,
    DivisionByZeroError,
    DoubleSlashTypeError,
    PercentTypeError,
)
from src.is_number import is_number


def calculate_in_rpn(lst_rpn) -> float:
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
    if not isinstance(lst_rpn, list):
        raise ValueError("Ошибка: входные данные должны быть списком")
    
    stack = []
    for token in lst_rpn:
        if is_number(token):
            stack.append(float(token))
            continue
        
        if token == "u-":
            if not stack:
                raise ValueError("Ошибка ОПН: унарный минус не имеет операнда")
            a = stack.pop()
            stack.append(-a)
            continue

        if token in ("+", "-", "*", "/", "^", "//", "%"):
            if len(stack) < 2:
                raise ValueError(f"Ошибка ОПН: оператор {token} не имеет двух операндов")
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
                    raise DivisionByZeroError(f"Нельзя делить на ноль")
                stack.append(a / b)

            elif token == "^":
                if a == 0 and b == 0:
                    raise ValueError("Ошибка: 0 в степени 0 не определено")
                stack.append(a**b)

            elif token == "//":
                if not (a.is_integer() and b.is_integer()):
                    raise DoubleSlashTypeError(
                        "Операция // поддерживается только для целых чисел"
                    )
                if b == 0:
                    raise DivisionByZeroError(f"Нельзя делить на ноль")
                stack.append(float(int(a) // int(b)))
            elif token == "%":
                if not (a.is_integer() and b.is_integer()):
                    raise PercentTypeError(
                        "Операция % поддерживается только для целых чисел"
                    )
                if b == 0:
                    raise DivisionByZeroError(f"Нельзя делить на ноль")
                stack.append(float(int(a) % int(b)))
            continue

        raise InvalidOperatorError(f"Недопустимый оператор: {token}")

    if len(stack) != 1:
        raise ValueError("Ошибка ОПН: неверное количество операндов")

    return stack[0]
