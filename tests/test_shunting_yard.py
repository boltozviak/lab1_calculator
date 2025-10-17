import pytest
from calculator_functions.shunting_yard import ShunringYardAlgorithm
from calculator_functions.tokenizer import Token
from calculator_functions.errors import ParsingError

@pytest.mark.parametrize(
    ("values", "expected_values"),
    [
        pytest.param([2, '+', 2], [2, 2, '+']),
        pytest.param([3, '*', 1, '+', 20], [3, 1, '*', 20, '+']),
        pytest.param(['(', 2, '+', 2, ')', '*', 2], [2, 2, '+', 2, '*']),
        pytest.param([2, '**', 3, '**', 2], [2, 3, 2, '**', '**']),  # right-assoc
        pytest.param([10, '//', 3], [10, 3, '//']),
        pytest.param([10, '%', 3], [10, 3, '%']),
        pytest.param(['~', 5, '+', 10], [5, '~', 10, '+']),
    ]
)
def test_shunting_yard_success(values, expected_values):
    algorithm = ShunringYardAlgorithm()
    tokens = [Token(v, i) for i, v in enumerate(values)]
    rpn = algorithm.shunting_yard(tokens)
    assert [t.value for t in rpn] == expected_values

@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param(['(', 1, '+', 2], "Unbalanced brackets error: ( at position 0"),
        pytest.param([1, '+', 2, ')'], "Unbalanced brackets error: ) at position 3"),
        pytest.param([1, '&', 2], "Unknown operator error: & at position 1"),
    ]
)
def test_shunting_yard_exceptions(values, expected):
    algorithm = ShunringYardAlgorithm()
    tokens = [Token(v, i) for i, v in enumerate(values)]
    with pytest.raises(ParsingError) as e_info:
        algorithm.shunting_yard(tokens)
    assert str(e_info.value) == expected
