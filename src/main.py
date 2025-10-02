class Calculator():
    def __init__(self):

        #можно реализовать через import operator
        self.OPERATORS = {
            '+': (lambda x, y: x + y, 1, 'left', False),
            '-': (lambda x, y: x - y, 1, 'left', False),
            '*': (lambda x, y: x * y, 2, 'left', False),
            '/': (self._division, 2, 'left', False),
            '**': (lambda x, y: x ** y, 3, 'right', False),
            '//': (self._floor_division, 2, 'left', False),
            '%': (self._mod_division, 2, 'left', False),
            '~': (lambda x: -x, 4, 'left', True),
            '$': (lambda x: x, 4, 'left', True)
        }

        self.int_OPERATORS = {'//', '%'}

    def _division(self, x, y):
        """ """

        if y == 0:
            raise ValueError('Division by zero') # пока пусть будет if/else - позже поменять на try/except
        return x / y

    def _floor_division(self, x, y):
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Operator // requires integers")
        if y == 0:
            raise ValueError("Division by zero")
        return x // y

    def _mod_division(self, x, y):
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Operator % requires integers")
        if y == 0:
            raise ValueError("Division by zero")
        return x % y

    def parse(self, expression):
        tokens = []
        n = len(expression)
        i = 0

        while i < n:
            symbol = expression[i]

            if symbol.isspace():
                i += 1
                continue

            if symbol.isdigit() or (symbol == '.' and i + 1 < n and expression[i+1].isdigit()):
                j = i
                has_dot = False

                while j < n:
                    if expression[j].isdigit():
                        j += 1
                    elif expression[j] == '.' and not has_dot:
                        has_dot = True
                        j += 1
                    else:
                        break

                num_str = expression[i:j]
                if has_dot:
                    tokens.append(float(num_str))
                else:
                    tokens.append(int(num_str))
                i = j
                continue

            if symbol in '+-*/%()':
                if symbol in '+-':
                    if not tokens or tokens[-1] == '(':
                        if symbol == '+':
                            tokens.append('$')
                        elif symbol == '-':
                            tokens.append('~')
                    elif isinstance(tokens[-1], str) and tokens[-1] in self.OPERATORS and tokens[-1] != ')':
                        raise ValueError(f'Incorrect operator input: {tokens[-1],symbol}')
                    else:
                        tokens.append(symbol)
                else:
                    if symbol == '*' and i + 1 < n and expression[i+1] == '*':
                        tokens.append('**')
                        i += 1
                    elif symbol == '/' and i + 1 < n and expression[i+1] == '/':
                        tokens.append('//')
                        i += 1
                    else:
                        tokens.append(symbol)

                i += 1
                continue

            raise ValueError(f'Unknown symbol: {symbol}')

        return tokens

    def shunting_yard(self, tokens):
        output = []
        stack = []

        for token in tokens:
            if isinstance(token, (int, float)):
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ValueError('Unbalanced brackets')
                stack.pop()

            else:
                op_info = self.OPERATORS.get(token)
                if not op_info:
                    raise ValueError(f'\nUnknown operator: {token}')

                _, priority, associativity, _ = op_info

                while stack and stack[-1] != '(':
                    top_op = stack[-1]
                    if top_op not in self.OPERATORS:
                        break

                    top_priority = self.OPERATORS[top_op][1]

                    if (associativity == 'left' and priority <= top_priority) or \
                        (associativity == 'right' and priority < top_priority):
                        output.append(stack.pop())
                    else:
                        break

                stack.append(token)

        while stack:
            op = stack.pop()
            if op == '(':
                raise ValueError('Unbalanced brackets')
            output.append(op)

        return output

    def evaluate_rpn(self, rpn):
        stack = []

        for token in rpn:
            if isinstance(token, (int, float)):
                stack.append(token)
            else:
                op_func, _, _, is_unary = self.OPERATORS[token]

                if is_unary:
                    if len(stack) < 1:
                        raise ValueError('Not enough operands for a unary operator')
                    operand = stack.pop()

                    result = op_func(operand)
                    stack.append(result)
                else:
                    if len(stack) < 2:
                        raise ValueError("Not enough operands for a binary operator")

                    right = stack.pop()
                    left = stack.pop()
                    result = op_func(left, right)
                    stack.append(result)

        if len(stack) != 1:
            raise ValueError("Incorrect expression")

        return stack[0]

    def calculate(self, expression):
        try:
            tokens = self.parse(expression)
            if not tokens:
                return 0

            rpn = self.shunting_yard(tokens)

            result = self.evaluate_rpn(rpn)

            return result

        except Exception as e:
            raise ValueError(f"Calculation error {e}")

def main():
    calculator = Calculator()
    print("Console calculator")
    print("To exit, write: 'exit'")
    print("-" * 50)

    while True:
        try:
            expression = input('Enter the expression: ').strip()

            if expression.lower() == 'exit':
                print('Bye-bye!')
                break

            if not expression:
                continue

            result = calculator.calculate(expression)

            if isinstance(result, float):
                if result.is_integer():
                    print(f"Result: {int(result)}")
                else:
                    print(f"Result: {result}")
            else:
                print(f"Result: {result}")

        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
