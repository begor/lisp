import pytest

from lisp.parser import evaluate, parse


PROGRAM_2_RESULT = [
    ('()', None),
    ('(+ 2 3.2)', 5.2),
    ('(+ 2 (- 4 (* 2 1)))', 4),
    ('(+ (+ (+ 1 (+ 2 3)) 4 5 6) 7 (- 9 1) 9)', 45),
    ('(* 1 2 3 4 5)', 120)
]


@pytest.mark.parametrize('program, result', PROGRAM_2_RESULT)
def test_parses(program, result):
    ast = parse(program)
    assert evaluate(ast) == result
