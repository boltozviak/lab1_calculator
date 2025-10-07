from typing import Any, List, Union

class ParsingError(Exception):

    def __init__(self, message: str, position: None | int, error_type: str = 'Parsing'):
        super().__init__(message)
        self.message = message
        self.position = position
        self.error_type = error_type

    def __str__(self):
        if self.position is not None:
            return f"{self.error_type} error: {self.message} at position {self.position}"
        return f"{self.error_type} error: {self.message}"

class Token():
    def __init__(self, value: Any, position: int):
        self.value = value
        self.position = position

class Calculator():
    def __init__(self):

        self.operators = {
            '+': (lambda x, y: x + y, 1, 'left', False),
            '-': (lambda x, y: x - y, 1, 'left', False),
            '*': (lambda x, y: x * y, 2, 'left', False),
            '/': (self._division, 2, 'left', False),
            '**': (lambda x, y: x ** y, 5, 'right', False),
            '//': (self._floor_division, 2, 'left', False),
            '%': (self._mod_division, 2, 'left', False),
            '~': (lambda x: -x, 4, 'left', True),
            '$': (lambda x: x, 4, 'left', True)
        }

    def _division(self, x: Union[int,float], y: Union[int,float]) -> float:
        if y == 0:
            raise ValueError('Division by zero')
        return x / y

    def _floor_division(self, x: int, y: int) -> int:
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Operator // requires integers")
        if y == 0:
            raise ValueError("Division by zero")
        return x // y

    def _mod_division(self, x: int, y: int) -> int:
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Operator % requires integers")
        if y == 0:
            raise ValueError("Division by zero")
        return x % y

    def parser(self, expression: str) -> List[Token]:
        tokens = []
        n = len(expression)
        i = 0

        while i < n:
            symbol = expression[i]

            if symbol.isspace():
                i += 1
                continue

            if symbol.isdigit():
                j = i
                has_dot = False

                while j < n:
                    if expression[j].isdigit():
                        j += 1
                    elif expression[j] == '.' and j + 1 < n and expression[j+1].isdigit() and not has_dot:
                        has_dot = True
                        j += 1
                    else:
                        break

                num_str = expression[i:j]
                try:
                    if has_dot:
                        token_value = float(num_str)
                    else:
                        token_value = int(num_str)
                    tokens.append(Token(token_value, i))
                except ValueError:
                    raise ParsingError(num_str, i, 'Invalid number format')

                i = j
                continue

            if symbol in '+-*/%()':
                if symbol in '+-':
                    if not tokens or tokens[-1] == '(':
                        if symbol == '+':
                            tokens.append(Token('$', i))
                        elif symbol == '-':
                            tokens.append(Token('~', i))
                    elif isinstance(tokens[-1], str) and tokens[-1] in self.operators and tokens[-1] != ')':
                        raise ParsingError(f"Incorrect operator sequence '{tokens[-1].value}' followed by '{symbol}'", i)
                    else:
                        tokens.append(Token(symbol, i))
                else:
                    if symbol == '*' and i + 1 < n and expression[i+1] == '*':
                        tokens.append(Token('**', i))
                        i += 1
                    elif symbol == '/' and i + 1 < n and expression[i+1] == '/':
                        tokens.append(Token('//', i))
                        i += 1
                    else:
                        tokens.append(Token(symbol, i))

                i += 1
                continue

            raise ParsingError(f'{symbol}', i, 'Unknown symbol')

        return tokens

    def shunting_yard(self, tokens: List[Token]) -> List[Token]:
        output = []
        stack = []

        for token in tokens:
            if isinstance(token.value, (int, float)):
                output.append(token)
            elif token.value == '(':
                stack.append(token)
            elif token.value == ')':
                while stack and stack[-1].value != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ParsingError('Unbalanced brackets', token.position)
                stack.pop()

            else:
                op_info = self.operators.get(token.value)
                if not op_info:
                    raise ParsingError(f'\n{token.value}', token.position, 'Unknown operator')

                _, priority, associativity, _ = op_info

                while stack and stack[-1].value != '(':
                    top_op = stack[-1]
                    if top_op not in self.operators:
                        break

                    top_priority = self.operators[top_op][1]

                    if (associativity == 'left' and priority <= top_priority) or \
                        (associativity == 'right' and priority < top_priority):
                        output.append(stack.pop())
                    else:
                        break

                stack.append(token)

        while stack:
            op_token = stack.pop()
            if op_token.value == '(':
                raise ParsingError("Unbalanced brackets", op_token.position)
            output.append(op_token)

        return output

    def evaluate_of_rpn(self, rpn: List[Token]) -> Union[int, float]:
        stack = []

        for token in rpn:
            if isinstance(token.value, (int, float)):
                stack.append(token.value)
            else:
                op_func, _, _, is_unary = self.operators[token.value]

                if is_unary:
                    if len(stack) < 1:
                        raise ValueError(f'Not enough operands for a unary operator {token.position}')
                    operand = stack.pop()
                    result = op_func(operand)
                    stack.append(result)
                else:
                    if len(stack) < 2:
                        raise ValueError(f"Not enough operands for a binary operator at position {token.position}")
                    right = stack.pop()
                    left = stack.pop()
                    result = op_func(left, right)
                    stack.append(result)

        if len(stack) != 1:
            raise ValueError("Invalid expression - too many operators")

        return stack[0]

    def calculate(self, expression: str) -> Union[int, float]:
        try:
            tokens = self.parser(expression)
            if not tokens:
                return 0

            rpn = self.shunting_yard(tokens)

            result = self.evaluate_of_rpn(rpn)

            return result

        except ParsingError:
            raise
        except ValueError as e:
            raise ValueError(f"Calculation error {e}")

def main():
    calculator = Calculator()
    print("Calculator")
    print("To exit, write: 'exit'")
    print("-" * 50)

    while True:
        try:
            expression = input('Enter the expression: ').strip()

            if expression.lower() == 'exit':
                print('Bye-bye!')
                break

            if not expression:
                raise ValueError('Empty expression')

            result = calculator.calculate(expression)

            if isinstance(result, float):
                if result.is_integer:
                    print(f"Result: {int(result)}")
                else:
                    print(f"Result: {result}")
            else:
                print(f"Result: {result}")

        except (ParsingError, ValueError) as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
