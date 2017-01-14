import pytest

from lisp.parser import evaluate, parse, DEFAULT_ENV

parametrize = pytest.mark.parametrize


PROGRAM_2_RESULT = [
    ('()', []),
    ('(+ 2 3.2)', 5.2),
    ('(+ 2 (- 4 (* 2 1)))', 4),
    ('(+ (+ (+ 1 (+ 2 3)) 4 5 6) 7 (- 9 1) 9)', 45),
    ('(* 1 2 3 4 5)', 120),
    ('(cons 1 (cons 2 (cons 3 ())))', [1, 2, 3]),
    ('(car (cons 1 (cons 2 ())))', 1),
    ('(cdr (cons 1 (cons 2 ())))', [2]),
    ('(cdr (cons 1 (cons 2 (cons 3 ()))))', [2, 3]),
    ('(list 1 2 3 4 5)', [1, 2, 3, 4, 5]),
    ('(car (list (cons 1 (cons 2 ())) 3 4 5))', [1, 2]),
    ('(let ((x (cons 1 (cons 2 ())))) (car x))', 1),
    ('(define x (cons 1 (cons 2 (cons 3 ()))))', [1, 2, 3]),
    ('(let ((f (lambda (x) (* x 2)))) (f 2))', 4),
    ("""
    (let ((f (lambda
             (x)
             (let ((y 2)) (* x y))))) (f 2))
     """, 4),
    ("""
    (let ((f (lambda
             (x)
             (let ((y (cons 2 (cons 3 ())))) (cons x y))))) (f 1))
     """, [1, 2, 3]),
    ("""
    (let ((f (lambda
             (x)
             (let ((y (cons 2 (cons 3 ())))) (* x
                                                (car y)))))) (f 2))
     """, 4),
]


ENV_PROGRAM_RESULT = [
    ({**DEFAULT_ENV, **{'xs': [1, [2, [3, []]]]}}, '(car xs)', 1)
]


@parametrize('program, result', PROGRAM_2_RESULT)
def test_evaluates(program, result):
    ast = parse(program)
    assert evaluate(ast) == result


@parametrize('env, program, result', ENV_PROGRAM_RESULT)
def test_evaluates_with_env(env, program, result):
    ast = parse(program)
    assert evaluate(ast, env) == result
