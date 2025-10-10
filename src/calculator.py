from typing import Any

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
    """
    An expression calculator that parses an infix arithmetic expression,
    converts it to Reverse Poland Notation (RPN) using the shunting-yard algorithm
    and evaluate a result

    """


    def __init__(self):

        self.operators = {
            '+': (lambda x, y: x + y, 1, 'left'),
            '-': (lambda x, y: x - y, 1, 'left'),
            '*': (lambda x, y: x * y, 2, 'left'),
            '/': (self._division, 2, 'left'),
            '**': (self._power, 4, 'right'),
            '//': (self._floor_division, 2, 'left'),
            '%': (self._mod_division, 2, 'left'),
            '~': (lambda x: -x, 5, 'left'),
            '$': (lambda x: x, 5, 'left')
        }

    def _division(self, x: int | float, y: int | float) -> float:
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

    def _power(self, x: int | float, y: int | float) -> int | float:
        if x < 0 and isinstance(y, float):
            raise ValueError('Negative number under the root')
        if y > 1000:
            raise ValueError('Too high a power to be raised')
        return x ** y

    def parser(self, expression: str) -> list[Token]:
        """
        Tokenizes an infix expression into a list of tokens

        Arguments:
            expression (str): raw infix expression

        Return:
            List[Token]: a sequence of tokens representing numbers, operators and brackets

        Exceptions:
            ParsingError:
                - Unknown symbol
                - Invalid number format
                - Incorrect operator sequence
        """

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
                    elif expression[j] == '.' and j + 1 < n and expression[j+1].isdigit() and not has_dot:
                        has_dot = True
                        j += 1
                    else:
                        break

                num_str = expression[i:j]
                if len(num_str) > 10:
                    raise ParsingError('Number has more than 10 digits',i,'Invalid number format')
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
                    if not tokens or tokens[-1].value == '(':
                        if symbol == '+':
                            tokens.append(Token('$', i))
                        elif symbol == '-':
                            tokens.append(Token('~', i))
                    elif isinstance(tokens[-1].value, str) and tokens[-1].value in self.operators and \
                          tokens[-1].value != ')':
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

    def shunting_yard(self, tokens: list[Token]) -> list[Token]:
        """
        Converts a list of infix tokens to Reverse Polish Notation (RPN)
        using the shunting-yard algorithm

        Arguments:
            tokens (List[Token]): infix tokens

        Return:
            List[Token]: tokens in RPN order

        Exceptions:
            ParsingError:
                - Unbalanced brackets
                - Unknown operator
        """

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
                    raise ParsingError(token.value,token.position,'Unbalanced brackets')
                stack.pop()

            else:
                op_info = self.operators.get(token.value)
                if not op_info:
                    raise ParsingError(token.value, token.position, 'Unknown operator')

                _, priority, associativity = op_info

                while stack and stack[-1].value != '(':
                    top_token = stack[-1]
                    top_op_info = self.operators.get(top_token.value)
                    if top_op_info is None:
                        break

                    top_priority = top_op_info[1]

                    if (associativity == 'left' and priority <= top_priority) or \
                        (associativity == 'right' and priority < top_priority):
                        output.append(stack.pop())
                    else:
                        break

                stack.append(token)

        while stack:
            op_token = stack.pop()
            if op_token.value == '(':
                raise ParsingError(op_token.value, op_token.position, "Unbalanced brackets")
            output.append(op_token)

        return output

    def evaluate_of_rpn(self, rpn: list[Token]) -> int | float:
        """
        Evaluates an expression given in Reverse Polish Notation (RPN).

        Parameters:
            rpn (List[Token]): tokens in RPN order.

        Returns:
            int | float: Computed result.

        Exceptions:
            ParsingError:
                - Not enough operands for operation
                - If final stack contain more than one result
            ValueError:
                - Arithemtic errors inside operators
        """

        stack = []

        for token in rpn:
            if isinstance(token.value, (int, float)):
                stack.append(token.value)
            else:
                op_func, _, _ = self.operators[token.value]

                if token.value in '$~':
                    if len(stack) < 1:
                        raise ParsingError(f'Not enough operands for a unary operator {token.value}',\
                                            token.position, 'Calculation')
                    operand = stack.pop()
                    result = op_func(operand)
                    stack.append(result)
                else:
                    if len(stack) < 2:
                        raise ParsingError(f'Not enough operands for a binary operator {token.value}',\
                                            token.position, 'Calculation')
                    right = stack.pop()
                    left = stack.pop()
                    result = op_func(left, right)
                    stack.append(result)

        if len(stack) != 1:
            raise ParsingError("Too many operands", None, 'Invalid expression')

        return stack[0]

    def calculate(self, expression: str) -> int | float:
        """
        Parses, compiles to RPN, and evaluates an infix arithmetic expression.

        Parameters:
            expression (str): raw infix expression.

        Returns:
            int | float: computed result.

        Exceptions:
            - Empty expression
            - Issues during parsing of shunting-yard
            - Calculation errors
        """

        try:
            tokens = self.parser(expression)
            if not tokens:
                raise ParsingError("Empty expression", 0, 'Invalid expression')

            rpn = self.shunting_yard(tokens)

            result = self.evaluate_of_rpn(rpn)

            return result

        except ParsingError:
            raise
        except ValueError as e:
            raise ParsingError(f"{e}", 0, 'Calculation')
