from src.infix_to_postfix import infix_to_postfix
from src.clculate import calculate_in_rpn
from src.errors import (
    InvalidOperatorError,
    DivisionByZeroError,
    PercentTypeError,
    DoubleSlashTypeError,
    NoOperatorBetweenNumbersError,
    TwooperatorsStraightError,
    NumAndBracketError,
)


def main() -> None:
    expr = input("Введите инфиксное выражение: ")
    try:
        postfix = infix_to_postfix(expr)
        print("Постфиксная запись:", " ".join(postfix))
        print("Ответ:", calculate_in_rpn(postfix))
    except InvalidOperatorError as e:
        print(f"Ошибка: недопустимый оператор: {e}")
    except DivisionByZeroError:
        print("Ошибка: деление на ноль")
    except PercentTypeError as e:
        print(
            f"Ошибка: операция % не поддерживается для типа {e.type_}, используйте только целые числа"
        )
    except DoubleSlashTypeError as e:
        print(
            f"Ошибка: операция // не поддерживается для типа {e.type_}, используйте только целые числа"
        )
    except ValueError:
        print("Ошибка: неверный формат числа")
    except NoOperatorBetweenNumbersError:
        print("Ошибка: отсутствует оператор между числами")
    except TwooperatorsStraightError:
        print("Ошибка: два оператора идут подряд")
    except NumAndBracketError:
        print("Ошибка: число и открывающая/закрывающая скобка идут подряд")
    except Exception as e:
        print(f"Другая ошибка: {e}")


if __name__ == "__main__":
    main()
