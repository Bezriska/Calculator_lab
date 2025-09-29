from src.is_number import is_number


def check_operators(token) -> bool:
    """Проверяет, что между двумя числами есть оператор.

    Args:
        token (str): текущий токен

    Returns:
        bool: True, если между двумя числами есть оператор, иначе False.
    """
    for i in range(len(token) - 1):
        if is_number(token[i]) and is_number(token[i + 1]):
            return False
    return True


def check_numbers(tokens) -> bool:
    """Проверяет, что между двумя операторами есть число.

    Args:
        token (str): текущий токен

    Returns:
        bool: True, если между двумя операторами есть число, иначе False.
    """
    ops = ("+", "-", "*", "/", "^", "//", "%")
    for i in range(len(tokens) - 1):
        for i in range(len(tokens) - 1):
            left = tokens[i]
            right = tokens[i + 1]
            if left in ops and right in ops:
                return False
            # исключаем случаи скобок: ( ) и пр.
            if left not in ops and right not in ops:
            # оба не оператора — это handled в check_operators
                continue
    return True


def check_open_bracket(tokens) -> bool:
    """Проверяет, что между числом и открывающей\закрывающей скобками есть оператор.

    Args:
        tokens (str): текущий токен

    Returns:
        bool: True, если между числом и открывающей\закрывающей скобками есть оператор, иначе False.
    """
    for i in range(len(tokens) - 1):
        if is_number(tokens[i]) and tokens[i + 1] == "(":
            return False
        if tokens[i] == ")" and is_number(tokens[i + 1]):
            return False
    return True
