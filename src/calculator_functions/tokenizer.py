from .tokens import Token
from .errors import ParsingError
from .constants import OPERATORS, MAX_LENGTH_OF_NUMBER, CHARS_OF_OPERATOR

class Tokenizer:
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
                        elif expression[j] == '.':
                            if has_dot:
                                raise ParsingError("Invalid number format", j, "Invalid number format")
                            if j + 1 < n and expression[j+1].isdigit():
                                has_dot = True
                                j += 1
                            else:
                                raise ParsingError("Invalid number format", j, "Invalid number format")
                        else:
                            break

                    num_str = expression[i:j]
                    if len(num_str) > MAX_LENGTH_OF_NUMBER:
                        raise ParsingError('Number has more than 10 digits',i,'Invalid number format')
                    token_value: int | float
                    try:
                        token_value = int(num_str)
                    except ValueError:
                        token_value = float(num_str)

                    tokens.append(Token(token_value, i))

                    i = j
                    continue

                if symbol in CHARS_OF_OPERATOR:
                    if symbol in '+-':
                        if not tokens or tokens[-1].value == '(':
                            if symbol == '+':
                                tokens.append(Token('$', i))
                            elif symbol == '-':
                                tokens.append(Token('~', i))
                        elif isinstance(tokens[-1].value, str) and tokens[-1].value in OPERATORS and \
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
