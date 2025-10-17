from .tokenizer import Tokenizer
from .shunting_yard import ShunringYardAlgorithm
from .evaluator import EvaluatorRPN
from .errors import ParsingError

class Calculator:
    """
    An expression calculator that parses an infix arithmetic expression,
    converts it to Reverse Poland Notation (RPN) using the shunting-yard algorithm
    and evaluate a result

    """
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.shunting_yard = ShunringYardAlgorithm()
        self.evaluator = EvaluatorRPN()

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
            tokens = self.tokenizer.parse_tokens(expression)
            if not tokens:
                raise ParsingError("Empty expression", 0, 'Invalid expression')

            rpn = self.shunting_yard.shunting_yard(tokens)

            result = self.evaluator.evaluate_of_rpn(rpn)

            return result

        except ParsingError:
            raise
        except ValueError as e:
            raise ParsingError(f"{e}", 0, 'Calculation')
