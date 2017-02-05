# (lisp)

[![Build Status](https://travis-ci.org/begor/lisp.svg?branch=master)](https://travis-ci.org/begor/lisp)

A simple interpreter for a [Scheme](https://www.gnu.org/software/mit-scheme/)-like language built in Python3.

## What it can do?
*WIP*

## How to do it?

- REPL
```
mbpro:lisp begor$ python lisp

(lisp) - a minimalistic LISP interpreter.
(lisp)> (+ 2 3)
5
```
- Reading and interpreting files
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
- Tests
```
mbpro:lisp begor$ pytest tests/
============================= test session starts ==============================

tests/unit/env_test.py ....
tests/unit/eval_test.py .................................
tests/unit/parser_test.py .......

========================== 44 passed in 0.07 seconds ===========================
```
