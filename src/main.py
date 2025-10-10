from calculator import Calculator, ParsingError

def main():
    calculator = Calculator()
    print("Calculator")
    print("To exit, write: 'exit'")
    print("-" * 50)

    while True:
        try:
            expression = input('Enter the expression: ')

            if expression.lower() == 'exit':
                print('Bye-bye!')
                break

            result = calculator.calculate(expression)

            if isinstance(result, float):
                if result.is_integer():
                    print(f"Result: {int(result)}")
                else:
                    print(f"Result: {result}")
            else:
                print(f"Result: {result}")

        except (ParsingError, ValueError) as e:
            print(f"{e}")

if __name__ == "__main__":
    main()
