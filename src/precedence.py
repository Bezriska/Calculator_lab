def precedence(op) -> int:
    """Проверяет приоритет оператора

    Args:
        op (str): текущий оператор

    Returns:
        int: приоритет оператора
    """
    if op in ("+", "-"):
        return 1
    if op in ("*", "/", "//", "%"):
        return 2
    if op == "^":
        return 3
    if op == "u-":
        return 4
    return 0
