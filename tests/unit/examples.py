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
    ('(list? (list 1 2 3 4 5))', True),
    ('(atom? 4)', True),
    ('(number? 4)', True),
    ('(atom? (list 1 2 3))', False),
    ('(number? (quote symbol))', False),
    ('(symbol? (quote symbol))', True),
    ('(quote (cons 1 (list 2 3 4)))', ['cons', 1, ['list', 2, 3, 4]]),
    ('(quasiquote (0 (unquote (+ 1 2)) 4))', [0, 3, 4]),
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
    ("""
     (let ((f (lambda (xs)
                (if (list? xs)
                    (sum xs)
                    xs))))
            (f (list 1 2 3 4 5)))
     """, 15),
    ("""
     (let ((f (lambda (xs)
                (if (list? xs)
                    (sum xs)
                    xs))))
            (f 15))
     """, 15),
    ("""
     (let ((x (* 3 5))
           (y 15))
            (eq? x y))
     """, True),
    ("""
     (let ((x 2))
        (let ((y (set! x (* x x))))
            (* x y)))
     """, 16),
    ("""
     (cond ((> 3 2) 42)
            ((< 3 2) -1))
     """, 42),
    ("""
     (cond ((< 3 2) 42)
            ((> 3 2) -1))
     """, -1),
    ("""
     (cond ((< 3 2) 42)
            ((= 3 2) -1))
     """, []),
    ("""
     (cond ((< 3 2) 42)
            ((= 3 2) -1)
            (#t 1))
     """, 1),
    ("""
     (filter (lambda (x) (= x 2)) (list 1 2 3 4 5))
     """, [2]),
    ("""
     (filter (lambda (x) (> x 20)) (list 1 2 3 4 5))
     """, []),
    ("""
     (map (lambda (x) (* x 2)) (list 1 2 3 4 5))
     """, [2, 4, 6, 8, 10]),
    ("""
     (fold + (list 1 2 3 4 5))
     """, 15),
    ("""
     (sum (list 1 2 3 4 5))
     """, 15),
    ("""
     (mul (list 1 2 3))
     """, 6),
    ("""
     (define map (lambda (fn xs)
                    (reverse (fold (lambda (xs x) (cons (fn x) xs)) xs ()))))

     (map (lambda (x) (* x 2)) (list 1 2 3 4 5))
     """, [2, 4, 6, 8, 10]),
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
