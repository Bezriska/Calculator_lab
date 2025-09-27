def is_operator(token):
    """Проверяет, что токен является оператором

    Args:
        token (str): текущий токен

    Returns:
        bool: True, если токен является оператором, иначе False
    """
    return token in ("+", "-", "*", "/", "^", "u-", "//", "%")
