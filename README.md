# CALCULATOR
## MAI - Python programming - LAB1
An expression calculator that parses an infix arithmetic expression,
converts it to Reverse Poland Notation (RPN) using the shunting-yard algorithm
and evaluate a result
### features
+, -, *, /, ** (right-associativity), // (requires integers), % (requires integers), ()

## Run
```powershell
python -m src.main
#I don't know how run tests - I use "pytest -q"
```
## Assumptions
- 0 ** 0 = 1
- The user can write the expression directly in RPN
- .5 -> 0.5
- The unary character only works at the beginning of a line or in brackets, otherwise an error occurs
- The unary character is a separate token
- Number length must be less than 10 digits
- The expression can contain leading zeros

## Questions for Samir
- Add an exception for large powers
- Operators - Should it be moved to a constants of class?
- PYTHONPATH - how to do it right?(+what do with pytest.ini, .env)

## References
- https://habr.com/ru/articles/908062/ - All about shunting-yard
- https://dronperminov.ru/articles/math-expressions-parsing-in-vanilla-javascript-part-one-tokenization - calculator on js
- https://habr.com/ru/articles/273253/ -  parsing in 50 strings
- https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D1%81%D0%BE%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%BE%D1%87%D0%BD%D0%BE%D0%B9_%D1%81%D1%82%D0%B0%D0%BD%D1%86%D0%B8%D0%B8 - shunting-yard algorithm
