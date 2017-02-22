# (lisp)

[![Build Status](https://travis-ci.org/begor/lisp.svg?branch=master)](https://travis-ci.org/begor/lisp)

## TL;DR

A simple interpreter for a [Scheme](https://www.gnu.org/software/mit-scheme/)-like language built in Python3.

## What it can do?
*(lisp)* has a set of essential Lisp special forms and build-in functions:

Special forms:
- `let`
- `define`
- `if`
- `cond`
- `set!`
- `quote`
- `quasiquoute`
- `unqote`

Built-in functions:
- Standard arithmetic and comparison: `+`, `*`, `>`, `<=`, `abs`, ...
- Classic Lisp: `cons`, `car`, `cdr`, `list`, `eq?`
- Short-circuit logic: `and`, `or`
- Introspection: `function?`, `list?`, `atom?`, `number?`, `symbol?`
- List processing: `map`, `filter`, `fold`, `sum`, `reverse`, `mul`

## How to use it?

*(lisp)* comes with a simple REPL and ability to read and evaluate programs from files.

- REPL
```
mbpro:lisp begor$ python lisp
(lisp) - a minimalistic LISP interpreter.
(lisp)> (define square (lambda (x) (* x x)))
<function procedure.<locals>.<lambda> at 0x7fdff9940598>
(lisp)> (square 42)

1764
```
- Files
```
mbpro:lisp begor$ cat examples/fact.lisp
(define fact
  (lambda (n)
    (if (<= n 1)
      1
      (* n
        (fact (- n 1))))))

(fact 100)

mbpro:lisp begor$ python lisp examples/fact.lisp
93326215443944152681699238...
```

## Any tests?
```
mbpro:lisp begor$ pytest tests/
======================================= test session starts ========================================

tests/unit/env_test.py ....
tests/unit/eval_test.py ............................................
tests/unit/parser_test.py ........

==================================== 56 passed in 0.07 seconds =====================================

```
