import pytest

from lisp.parser import parse


PROGRAM_2_AST = [
    ('()', []),
    ('(+ 2 3.2)', ['+', 2, 3.2]),
    ('(+ 2 (- 4 (* 2 1)))', ['+', 2, ['-', 4, ['*', 2, 1]]]),
    ('(+ (+ (+ 1 (+ 2 3)) 4 5 6.2) -7 (- 9 1) 8)',
     ['+', ['+', ['+', 1, ['+', 2, 3]], 4, 5, 6.2], -7, ['-', 9, 1], 8])
]


@pytest.mark.parametrize('program, ast', PROGRAM_2_AST)
def test_parses(program, ast):
    assert parse(program) == ast
