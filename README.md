# CALCULATOR
## MAI - Python programming - LAB1
An expression calculator that parses an infix arithmetic expression,
converts it to Reverse Poland Notation (RPN) using the shunting-yard algorithm
and evaluate a result

## Features
Calculator can works with integer/float numbers and such operators as +, -, *, /, ** (right-associativity), // (requires integers), % (requires integers), (), unary +/-

## How it works
### Tokenizer

The tokenizer iterates over the expression and passes operators and numbers in the format [value; index] to the 'tokens' list.
The value is later used for calculations, and the index is used in error descriptions.

### Shunting Yard
The list of tokens is transformed into a list containing the Reverse Polish Notation of the expression by using the shunting yard algorithm
- If the token is a number, add it to the result output
- If the token is operator op1, then:
- - As long as there is an operator op2 on the top of the stack whose priority is higher than or equal to op1, and if the priorities are equal, op1 is left-associative
- - - Push op2 from the stack to the output
- - Push op1 onto the stack
- If the token is an opening bracket, then push it onto the stack
- If the token is a closing parenthesis
- - While the token on the top of the stack is not an opening brackets
- - - Push the operator from the stack to the output
- - Pop the opening bracket from the stack, but don't add it to the output

### Evaluator
Evaluate RPN by alternately pushing operands and operators onto the stack until a single number remains on the stack - the answer

### Calculator
Combines three classes into one

## Set up and Run
```zsh
#clone a repository
git clone <repository-url>
cd lab1_calculator

#install dependencies
uv sync

#Run a programm
python -m src.main

#Run tests
pytest -q # run all

pytest tests/test_shunting_yard.py # run a single test
```

## Assumptions
- 0 ** 0 = 1
- The user can write the expression directly in RPN
- .5 -> 0.5
- The unary character only works at the beginning of a line or in brackets, otherwise an error occurs
- The unary character is a separate token
- Number length must be less than 10 digits
- The expression can contain leading zeros
- Maximum power - 999

## References
- https://habr.com/ru/articles/908062/ - All about shunting-yard
- https://dronperminov.ru/articles/math-expressions-parsing-in-vanilla-javascript-part-one-tokenization - calculator on js
- https://habr.com/ru/articles/273253/ -  parsing in 50 strings
- https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D1%81%D0%BE%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%BE%D1%87%D0%BD%D0%BE%D0%B9_%D1%81%D1%82%D0%B0%D0%BD%D1%86%D0%B8%D0%B8 - shunting-yard algorithm
