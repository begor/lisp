from lisp.parser import parse

def test_parses():
    ast = parse('(+ 2 (- 4 (* 2 1)))')
    assert ast == ['+', 2, ['-', 4, ['*', 2, 1]]]
