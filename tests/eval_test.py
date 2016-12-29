import pytest

from lisp.parser import evaluate, parse


PROGRAM_2_RESULT = [
    ('()', []),
    ('(+ 2 3.2)', 5.2),
    ('(+ 2 (- 4 (* 2 1)))', 4),
    ('(+ (+ (+ 1 (+ 2 3)) 4 5 6) 7 (- 9 1) 9)', 45),
    ('(* 1 2 3 4 5)', 120),
    ('(cons 1 (cons 2 (cons 3 ())))', [1, [2, [3, []]]]),
    ('(car (cons 1 (cons 2 ())))', 1),
    ('(cdr (cons 1 (cons 2 ())))', [2, []]),
    ('(cdr (cons 1 (cons 2 (cons 3 ()))))', [2, [3, []]]),
    ('(let ((x (cons 1 (cons 2)))) (car x))', 1)
]


@pytest.mark.parametrize('program, result', PROGRAM_2_RESULT)
def test_parses(program, result):
    ast = parse(program)
    assert evaluate(ast) == result
