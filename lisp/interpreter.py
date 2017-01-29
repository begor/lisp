import functools

from lisp.parser import parse
from lisp.evaluator import evaluate, evaluate_ast


def compose(*fs):
    """
    Helper for convinient function composition.

    Example:
    f(g(t(args))) <-> compose(f, g, t)(args)
    """
    def compose2(f, g):
        return lambda *a, **kw: f(g(*a, **kw))

    return functools.reduce(compose2, reversed(fs))  # Need to revese!


interpreter = compose(parse, evaluate_ast, print)
