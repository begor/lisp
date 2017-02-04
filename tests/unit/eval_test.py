import pytest

from lisp.environment import default
from lisp.interpreter import evaluate_ast
from lisp.evaluator import evaluate_expression
from lisp.parser import parse
from examples import expression2result, environment_program2result


parametrize = pytest.mark.parametrize


def extend_environment(test):
    def wrapper(env, program, result):
        default.update(env)
        test(default, program, result)
    return wrapper


@parametrize('program, result', expression2result)
def test_evaluate_ast(program, result):
    ast = parse(program)
    assert evaluate_ast(ast) == result


@parametrize('env, program, result', environment_program2result)
@extend_environment
def test_evaluate_expression_with_env(env, program, result):
    ast = parse(program)
    assert evaluate_ast(ast, env) == result
