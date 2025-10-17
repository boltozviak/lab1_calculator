from .tokenizer import Token
from .errors import ParsingError
from .operators import BINARY_OPERATORS, UNARY_OPERATORS

class EvaluatorRPN:
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
                    if token.value in UNARY_OPERATORS:
                        op_func = UNARY_OPERATORS[token.value][0]
                        if len(stack) < 1:
                            raise ParsingError(f'Not enough operands for a unary operator {token.value}',\
                                                token.position, 'Calculation')
                        operand: int | float = stack.pop()
                        result = op_func(operand)
                        stack.append(result)
                    elif token.value in BINARY_OPERATORS:
                        op_binary_func = BINARY_OPERATORS[token.value][0]
                        if len(stack) < 2:
                            raise ParsingError(f'Not enough operands for a binary operator {token.value}',\
                                                token.position, 'Calculation')
                        right: int | float = stack.pop()
                        left: int | float = stack.pop()
                        result = op_binary_func(left, right)
                        stack.append(result)

            if len(stack) != 1:
                raise ParsingError("Too many operands", None, 'Invalid expression')

            return stack[0]
