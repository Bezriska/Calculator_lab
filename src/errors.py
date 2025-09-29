class CalculatorError(Exception):
    pass


class DivisionByZeroError(CalculatorError):
    def __init__(self):
        super().__init__("Ошибка: деление на ноль")


class InvalidOperatorError(CalculatorError):
    def __init__(self, operator):
        self.operator = operator
        super().__init__(f"Ошибка: недопустимый оператор: {operator}")


class DoubleSlashTypeError(CalculatorError):
    def __init__(self, type_):
        self.type_ = type_
        super().__init__(f"Ошибка: операция // не поддерживается для типа {type_}, используйте только целые числа")


class PercentTypeError(CalculatorError):
    def __init__(self, type_):
        self.type_ = type_
        super().__init__(f"Ошибка: операция % не поддерживается для типа {type_}, используйте только целые числа")


class NoOperatorBetweenNumbersError(CalculatorError):
    def __init__(self):
        super().__init__("Ошибка: отсутствует оператор между числами")


class TwooperatorsStraightError(CalculatorError):
    def __init__(self):
        super().__init__("Ошибка: два оператора идут подряд")


class NumAndBracketError(CalculatorError):
    def __init__(self):
        super().__init__("Ошибка: число и открывающая/закрывающая скобка идут подряд")
