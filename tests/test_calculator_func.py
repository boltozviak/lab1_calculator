import pytest
from calculator_functions.calculator import Calculator
from calculator_functions.calculator import ParsingError


@pytest.mark.parametrize(
    ('input', 'expected_result'),
    (
        pytest.param('2+2', 4),
        pytest.param('3 * 1 + 20', 23),
        pytest.param('2 + 2 * 2', 6),
        pytest.param('(2 + 2) * 2', 8),
        pytest.param('2 ** 2 ** 3', 256),
        pytest.param('-5 + 10', 5),
        pytest.param('+5 + 1', 6),
        pytest.param('-(-3)', 3),
        pytest.param('4/2', 2),
        pytest.param('7/2', 3.5),
        pytest.param('10%3', 1),
        pytest.param('10//3', 3),
        pytest.param('2 ** 0', 1),
        pytest.param('0 ** 2', 0),
        pytest.param('   43    -    13', 30),
        pytest.param('3 + 2.5', 5.5),
        pytest.param('5.0 - 2', 3),
        pytest.param('5.0  * 2', 10),
        pytest.param('10.0 / 4', 2.5),
        pytest.param('-0',0),
        pytest.param('+0',0),
        pytest.param('0.0000001 + 0.000002', 2.1e-06),
        pytest.param('(1+3)/(2.5-2)', 8),
        pytest.param('(((((((2 + 5))))) * 7)) + 0', 49)

    )
)
def test_calculate_func(input, expected_result):
    calculator = Calculator()
    assert calculator.calculate(input) == expected_result


@pytest.mark.parametrize(
    ('expression', 'expected_exception'),
    (
        pytest.param('2.', 'Invalid number format error: Invalid number format at position 1'),
        pytest.param('111111111111', 'Invalid number format error: Number has more than 10 digits at position 0'),
        pytest.param('2..2', 'Invalid number format error: Invalid number format at position 1'),
        pytest.param('1++2', "Parsing error: Incorrect operator sequence '+' followed by '+' at position 2"),
        pytest.param('1-*', 'Calculation error: Not enough operands for a binary operator * at position 2'),
        pytest.param('1&2', 'Unknown symbol error: & at position 1'),
        pytest.param('((1+2)', 'Unbalanced brackets error: ( at position 0'),
        pytest.param('(1+2))', 'Unbalanced brackets error: ) at position 5'),
        pytest.param('', 'Invalid expression error: Empty expression at position 0'),
        pytest.param('        ', 'Invalid expression error: Empty expression at position 0'),
        pytest.param('+', 'Calculation error: Not enough operands for a unary operator $ at position 0'),
        pytest.param('(-)', 'Calculation error: Not enough operands for a unary operator ~ at position 1'),
        pytest.param('1/0', 'Calculation error: Division by zero at position 0'),
        pytest.param('2/0.0', 'Calculation error: Division by zero at position 0'),
        pytest.param('2//0', 'Calculation error: Division by zero at position 0'),
        pytest.param('2%0', 'Calculation error: Division by zero at position 0'),
        pytest.param('4.5//5', 'Calculation error: Operator // requires integers at position 0'),
        pytest.param('4.5%5', 'Calculation error: Operator % requires integers at position 0'),
        pytest.param('5//2.5', 'Calculation error: Operator // requires integers at position 0'),
        pytest.param('5%2.5', 'Calculation error: Operator % requires integers at position 0'),
        pytest.param('(1.5+2.5)//2', 'Calculation error: Operator // requires integers at position 0'),
        pytest.param('(1+3)/(3-3)', 'Calculation error: Division by zero at position 0'),
        pytest.param('-2 ** 0.5', 'Calculation error: Negative number under the root at position 0'),
        pytest.param('2 ** 11111111', 'Calculation error: Too high a power to be raised at position 0'),

    )
)

def test_calculate_exceptions(expression, expected_exception):
    calculator = Calculator()
    with pytest.raises(ParsingError) as e_info:
        calculator.calculate(expression)
    assert str(e_info.value) == expected_exception
