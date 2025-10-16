import pytest
from calculator_functions.evaluator import EvaluatorRPN
from calculator_functions.tokens import Token
from calculator_functions.errors import ParsingError

@pytest.mark.parametrize(
    ("rpn_values", "expected"),
    [
        pytest.param([2, 2, '+'], 4),
        pytest.param([3, 1, '*', 20, '+'], 23),
        pytest.param([2, 2, '+', 2, '*'], 8),
        pytest.param([2, 3, 2, '**', '**'], 512),
        pytest.param([5, '~', 10, '+'], 5),
        pytest.param([5, '$', 1, '+'], 6),
        pytest.param([4, 2, '/'], 2.0),
        pytest.param([7, 2, '/'], 3.5),
        pytest.param([10, 3, '%'], 1),
        pytest.param([10, 3, '//'], 3),
    ]
)
def test_evaluator_success(rpn_values, expected):
    evaluator = EvaluatorRPN()
    rpn = [Token(v, i) for i, v in enumerate(rpn_values)]
    assert evaluator.evaluate_of_rpn(rpn) == expected

@pytest.mark.parametrize(
    ("rpn_values", "expected_exc", "expected"),
    [
        pytest.param(['$'], ParsingError, "Not enough operands for a unary operator"),
        pytest.param(['~'], ParsingError, "Not enough operands for a unary operator"),
        pytest.param(['+'], ParsingError, "Not enough operands for a binary operator"),
        pytest.param([2, '+'], ParsingError, "Not enough operands for a binary operator"),
        pytest.param([1, 2], ParsingError, "Too many operands"),
    ]
)
def test_evaluator_parsing_errors(rpn_values, expected_exception, expected):
    evaluator = EvaluatorRPN()
    rpn = [Token(v, i) for i, v in enumerate(rpn_values)]
    with pytest.raises(expected_exception) as e_info:
        evaluator.evaluate_of_rpn(rpn)
    assert expected in str(e_info.value)

@pytest.mark.parametrize(
    ("rpn_values", "expected_msg"),
    [
        pytest.param([1, 0, '/'], "Division by zero"),
        pytest.param([4.5, 5, '//'], "Operator // requires integers"),
        pytest.param([5, 2.5, '//'], "Operator // requires integers"),
        pytest.param([4.5, 5, '%'], "Operator % requires integers"),
        pytest.param([5, 2.5, '%'], "Operator % requires integers"),
        pytest.param([-2, 0.5, '**'], "Negative number under the root"),
        pytest.param([2, 10_000_000, '**'], "Too high a power to be raised"),
    ]
)
def test_evaluator_value_errors(rpn_values, expected):
    evaluator = EvaluatorRPN()
    rpn = [Token(v, i) for i, v in enumerate(rpn_values)]
    with pytest.raises(ValueError) as e_info:
        evaluator.evaluate_of_rpn(rpn)
    assert expected in str(e_info.value)
