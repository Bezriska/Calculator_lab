from src.infix_to_postfix import infix_to_postfix, tokenize, mark_unary
from src.calculate import calculate_in_rpn
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
        postfix = infix_to_postfix(mark_unary(tokenize(expr)))
        print("Токены:", tokenize(expr))
        print("Постфиксная запись:", postfix)
        print("Ответ:", calculate_in_rpn(postfix))
    except InvalidOperatorError as e:
        print(f"{e.operator}")
    except DivisionByZeroError:
        print("Ошибка: деление на ноль")
    except PercentTypeError as e:
        print(f"{e.type_}")
    except DoubleSlashTypeError as e:
        print(f"{e.type_}")
    except ValueError as e:
        print(f"{e}")
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
