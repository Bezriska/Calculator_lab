def is_number(token) -> bool:
    """Проверяет, что токен является числом

    Args:
        token (str): текущий токен

    Returns:
        bool: True, если токен является числом, иначе False
    """
    try:
        float(token)
        return True
    except ValueError:
        return False
