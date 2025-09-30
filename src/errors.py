class CalculatorError(Exception):
    pass


class DivisionByZeroError(CalculatorError):
    def __init__(self, message="Нельзя делить на ноль"):
        super().__init__(message)


class InvalidOperatorError(CalculatorError):
    def __init__(self, operator):
        self.operator = operator
        super().__init__(f"Ошибка: недопустимый оператор: {operator}")


class DoubleSlashTypeError(CalculatorError):
    def __init__(self, type_):
        self.type_ = type_
        super().__init__(
            f"Ошибка: операция // не поддерживается для типа {type_}, используйте только целые числа"
        )


class PercentTypeError(CalculatorError):
    def __init__(self, type_):
        self.type_ = type_
        super().__init__(
            f"Ошибка: операция % не поддерживается для типа {type_}, используйте только целые числа"
        )


class NoOperatorBetweenNumbersError(CalculatorError):
    def __init__(self, message="Ошибка: отсутствует оператор между числами"):
        super().__init__(message)


class TwooperatorsStraightError(CalculatorError):
    def __init__(self, message="Ошибка: два оператора идут подряд"):
        super().__init__(message)


class NumAndBracketError(CalculatorError):
    def __init__(
        self, message="Ошибка: число и открывающая/закрывающая скобка идут подряд"
    ):
        super().__init__(message)
