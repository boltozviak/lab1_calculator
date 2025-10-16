import pytest
from calculator_functions.tokenizer import Tokenizer
from calculator_functions.errors import ParsingError

@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        pytest.param("2+2", [(2, 0), ('+', 1), (2, 2)]),
        pytest.param("3 * 1 + 20", [(3, 0), ('*', 2), (1, 4), ('+', 6), (20, 8)]),
        pytest.param("2 ** 3", [(2, 0), ('**', 2), (3, 5)]),
        pytest.param("10//3", [(10, 0), ('//', 2), (3, 4)]),
        pytest.param("10%3", [(10, 0), ('%', 2), (3, 3)]),
        pytest.param("(2+2)*2", [('(', 0), (2, 1), ('+', 2), (2, 3), (')', 4), ('*', 5), (2, 6)]),
        pytest.param("-5 + 10", [('~', 0), (5, 1), ('+', 3), (10, 5)]),
        pytest.param("+5 + 1", [('$', 0), (5, 1), ('+', 3), (1, 5)]),
        pytest.param("3 + 2.5", [(3, 0), ('+', 2), (2.5, 4)]),
    ]
)
def test_tokenizer_success(expression, expected):
    tokenizer = Tokenizer()
    tokens = tokenizer.parser(expression)
    as_pairs = [(tok.value, tok.position) for tok in tokens]
    assert as_pairs == expected

@pytest.mark.parametrize(
    ("expression", "expected_str"),
    [
        pytest.param("2.", "Invalid number format error: Invalid number format at position 1"),
        pytest.param("2..2", "Invalid number format error: Invalid number format at position 1"),
        pytest.param("111111111111", "Invalid number format error: Number has more than 10 digits at position 0"),
        pytest.param("1++2", "Parsing error: Incorrect operator sequence '+' followed by '+' at position 2"),
        pytest.param("1&2", "Unknown symbol error: & at position 1"),
    ]
)
def test_tokenizer_errors(expression, expected_str):
    tokenizer = Tokenizer()
    with pytest.raises(ParsingError) as e_info:
        tokenizer.parser(expression)
    assert str(e_info.value) == expected_str
