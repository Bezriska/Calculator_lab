class CalculatorError(Exception):
    pass


class DivisionByZeroError(CalculatorError):
    def __init__(self):
        super().__init__()


class InvalidOperatorError(CalculatorError):
    def __init__(self, operator):
        self.operator = operator
        super().__init__(operator)


class DoubleSlashTypeError(CalculatorError):
    def __init__(self, type_):
        self.type_ = type_
        super().__init__(type_)


class PercentTypeError(CalculatorError):
    def __init__(self, type_):
        self.type_ = type_
        super().__init__(type_)


class NoOperatorBetweenNumbersError(CalculatorError):
    def __init__(self):
        super().__init__()


class TwooperatorsStraightError(CalculatorError):
    def __init__(self):
        super().__init__()


class NumAndBracketError(CalculatorError):
    def __init__(self):
        super().__init__()
