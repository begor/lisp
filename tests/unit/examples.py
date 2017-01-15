from lisp.environment import Env


expression2result = [
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
    ('(if (> 3 2) 4 5)', 4),
    ('(if (and (> 3 2) (= 0 1)) 4 5)', 5),
    ("""
    (let ((f (lambda
             (x)
             (let ((y 2)) (* x y))))) (f 2))
     """, 4),
    ("""
    (let ((f (lambda
             (x)
             (let ((y (cons 2 (cons 3 ())))) (cons x y)))))
        (f 1))
     """, [1, 2, 3]),
    ("""
    (let ((f (lambda
             (x)
             (let ((y (cons 2 (cons 3 ())))) (* x
                                                (car y))))))
         (f 2))
     """, 4),
]



environment_program2result = [
    ({'xs': [1, [2, [3, []]]]}, '(car xs)', 1),
    ({'xs': [1, [2, [3, []]]]},
    """
    (let ((f (lambda
             (alist)
             (* (car alist) 2))))
         (f xs))
     """,
     2),

]

environment_name2value = [
    [Env(names=('x',), values=(42,)),
     'x',
     42],
    [Env(names=('x', 'y'), values=(42, 84)),
     'x',
     42],
    [Env(names=('x', 'y'), values=(42, 84), outer=Env(names=('z',), values=(14,))),
     'z',
     14],
    [Env(names=('x', 'y', 'z'), values=(42, 84, 15), outer=Env(names=('z',), values=(14,))),
     'z',
     15]
]
