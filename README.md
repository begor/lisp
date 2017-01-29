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
mbpro:lisp begor$ cat examples/square.lisp
(let ((square (lambda (x) (* x x)))) (square 4))

mbpro:lisp begor$ python lisp examples/square.lisp
16
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
