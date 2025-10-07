import pytest
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from src.main import Calculator, ParsingError


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

    )
)
def test_calculate_ok(input, expected_result):
    calculator = Calculator()
    assert calculator.calculate(input) == expected_result

