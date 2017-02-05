from functools import reduce

from lisp.environment import default
from lisp.parser import parse
from lisp.evaluator import evaluate_expression, NIL


def compose(*fs):
    """
    Helper for convinient function composition.

    Example:
    f(g(t(args))) <-> compose(f, g, t)(args)
    """
    def compose2(f, g):
        return lambda *a, **kw: f(g(*a, **kw))

    return reduce(compose2, reversed(fs))  # Need to revese!


def evaluate_ast(ast, env=default):
    """
    Evaluate AST of s-expressions.
    """
    return reduce(lambda _, exp: evaluate_expression(exp, env), ast, NIL)


interpreter = compose(parse, evaluate_ast, print)
