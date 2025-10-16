import pytest
from calculator_functions.shunting_yard import ShunringYardAlgorithm
from calculator_functions.tokens import Token
from calculator_functions.errors import ParsingError

@pytest.mark.parametrize(
    ("infix_values", "expected_rpn_values"),
    [
        pytest.param([2, '+', 2], [2, 2, '+']),
        pytest.param([3, '*', 1, '+', 20], [3, 1, '*', 20, '+']),
        pytest.param(['(', 2, '+', 2, ')', '*', 2], [2, 2, '+', 2, '*']),
        pytest.param([2, '**', 3, '**', 2], [2, 3, 2, '**', '**']),  # right-assoc
        pytest.param([10, '//', 3], [10, 3, '//']),
        pytest.param([10, '%', 3], [10, 3, '%']),
        pytest.param(['~', 5, '+', 10], [5, '~', 10, '+']),
        pytest.param(['$', 5, '+', 1], [5, '$', 1, '+']),
    ]
)
def test_shunting_yard_success(infix_values, expected_rpn_values):
    algorithm = ShunringYardAlgorithm()
    tokens = [Token(v, i) for i, v in enumerate(infix_values)]
    rpn = algorithm.shunting_yard(tokens)
    assert [t.value for t in rpn] == expected_rpn_values

@pytest.mark.parametrize(
    ("infix_values", "expected_str"),
    [
        pytest.param(['(', 1, '+', 2], "Unbalanced brackets error: ( at position 0"),
        pytest.param([1, '+', 2, ')'], "Unbalanced brackets error: ) at position 3"),
        pytest.param([1, '&', 2], "Unknown operator error: & at position 1"),
    ]
)
def test_shunting_yard_errors(infix_values, expected_str):
    algorithm = ShunringYardAlgorithm()
    tokens = [Token(v, i) for i, v in enumerate(infix_values)]
    with pytest.raises(ParsingError) as e_info:
        algorithm.shunting_yard(tokens)
    assert str(e_info.value) == expected_str
