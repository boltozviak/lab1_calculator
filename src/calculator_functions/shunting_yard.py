from .tokens import Token
from .errors import ParsingError
from .constants import OPERATORS

class ShunringYardAlgorithm:
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
                    op_info = OPERATORS.get(token.value)
                    if not op_info:
                        raise ParsingError(token.value, token.position, 'Unknown operator')

                    _, priority, associativity = op_info

                    while stack and stack[-1].value != '(':
                        top_token = stack[-1]
                        top_op_info = OPERATORS.get(top_token.value)
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
