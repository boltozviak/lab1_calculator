MAX_LENGTH_OF_NUMBER = 10
MAX_POWER = 999
CHARS_OF_OPERATOR = '+-*/%()'

def _division(x: int | float, y: int | float) -> float:
        if y == 0:
            raise ValueError('Division by zero')
        return x / y

def _floor_division(x: int, y: int) -> int:
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Operator // requires integers")
        if y == 0:
            raise ValueError("Division by zero")
        return x // y

def _mod_division(x: int, y: int) -> int:
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Operator % requires integers")
        if y == 0:
            raise ValueError("Division by zero")
        return x % y

def _power(x: int | float, y: int | float) -> int | float:
        if x < 0 and isinstance(y, float):
            raise ValueError('Negative number under the root')
        if y > MAX_POWER:
            raise ValueError('Too high a power to be raised')
        return x ** y

BINARY_OPERATORS = {
    '+': (lambda x, y: x + y, 1, 'left'),
    '-': (lambda x, y: x - y, 1, 'left'),
    '*': (lambda x, y: x * y, 2, 'left'),
    '/': (_division, 2, 'left'),
    '**': (_power, 4, 'right'),
    '//': (_floor_division, 2, 'left'),
    '%': (_mod_division, 2, 'left'),
}

UNARY_OPERATORS = {
    '~': (lambda x: -x, 5, 'left'),
    '$': (lambda x: x, 5, 'left'),
}

OPERATORS = {**BINARY_OPERATORS, **UNARY_OPERATORS}
