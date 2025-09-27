from src.is_number import is_number


def check_operators(token):
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


def check_numbers(token):
    """Проверяет, что между двумя операторами есть число.

    Args:
        token (str): текущий токен

    Returns:
        bool: True, если между двумя операторами есть число, иначе False.
    """
    for i in range(len(token) - 1):
        if (
            not is_number(token[i])
            and not is_number(token[i + 1])
            and token[i] not in ("(", ")")
            and token[i + 1] not in ("(", ")")
            and (token[i] != '+' and token[i + 1] != '+')
            and (token[i] != '-' and token[i + 1] != '-')
        ):
            return False
    return True


def check_open_bracket(tokens):
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
