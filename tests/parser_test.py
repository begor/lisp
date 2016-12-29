import pytest

from lisp.parser import parse


PROGRAM_2_AST = [
    ('()', []),
    ('(+ 2 3.2)',
     ['+', 2, 3.2]),
    ('(+ 2 (- 4 (* 2 1)))',
     ['+', 2, ['-', 4, ['*', 2, 1]]]),
    ('(cons 1 (cons 2 (cons 3 ())))',
     ['cons', 1, ['cons', 2, ['cons', 3, []]]]),
    ('(car (cons 1 (cons 2 ())))',
     ['car', ['cons', 1, ['cons', 2, []]]]),
    ('(cdr (cons 1 (cons 2 ())))',
     ['cdr', ['cons', 1, ['cons', 2, []]]]),
    ('(let ((x (cons 1 (cons 2)))) (value x))',
    ['let', [['x', ['cons', 1, ['cons', 2]]]], ['value', 'x']])
]


@pytest.mark.parametrize('program, ast', PROGRAM_2_AST)
def test_parses(program, ast):
    assert parse(program) == ast
