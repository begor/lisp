import functools
import sys

from .environment import default, Env


NIL = []


def compose(*fs):
    """
    Helper for convinient function composition.

    Example:
    f(g(t(args))) <-> compose(f, g, t)(args)
    """
    def compose2(f, g):
        return lambda *a, **kw: f(g(*a, **kw))

    return functools.reduce(compose2, reversed(fs))


pretty_print = print


class F:
    """Representation of a 'function-object' with lexical scoping."""

    def __init__(self, args, body, env):
        """
        Initialize function object.
        Passing env allows to use lexical scoping.
        """

        self._body = body
        self._args = args
        self._env = env

    def __call__(self, *args):
        """
        Implementing 'function-object' as a functor.
        """

        env = Env(names=self._args, values=args, outer=self._env)
        return evaluate(self._body, env)


def tokenize(program):
    """
    I: (+ 2 (- 4 2))
    O: [(, +, 2, (, -, 4, 2, ), )]
    """
    return program.replace(')', ' ) ').replace('(', ' ( ').split()


def atomize(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token


def read(tokens):
    """
    Read stream of tokens, return AST.

    Tokens represented as a flat list.
    AST represented as a nested lists.

    Exaple:
    > read([(, +, 2, (, -, 4, 2, ), )])
    >> [+, 2, [-, 4, 2]]
    """

    def proceed_list(tokens):
        l = []
        while tokens[0] != ')':
            l.append(read(tokens))
        tokens.pop(0)
        return l

    if not len(tokens):
        raise SyntaxError('Empty program')

    t = tokens.pop(0)

    if t == '(':
        return proceed_list(tokens)
    elif t == ')':
        raise SyntaxError('Unexpected ) term')
    else:
        return atomize(t)


def to_bool(value):
    """
    """
    falsy = ['false', [], 0]  # TODO: not sure

    if value in falsy:
        return False

    return True


def evaluate(exp, env=default):
    """
    Evaluate expression exp in environment env.

    Expression represented as a list of terms.
    Environment as an instance of Env class.

    Example:
    > evaluate([+, 2, [-, 4, 2]], Env())  # Passing empty env
    >> 4
    """

    def let(bindings, body):
        """
        Handle let special form.

        First, extend current environment with bindings.
        Second, evaluate body under extended environment.
        """
        names = [b[0] for b in bindings]
        values = [evaluate(b[1], env) for b in bindings]
        new_env = Env(names=names, values=values, outer=env)
        return evaluate(body, new_env)

    def define(name, exp):
        """
        Handle define special form.

        First, evaluate exp under under current environment to a value V.
        Second, extend current environment with name -> V pair.

        Return V as a result.
        """
        val = evaluate(exp, env)
        env.update({name: val})
        return val

    def if_(predicate, if_true_exp, if_false_exp):
        """
        Handle if special form.

        First, evaluate predicate under current environment to a value V.
        Second, if V is truthy evaluate if_true_exp to a value V'.
        Otherwise, evaluate if_false_exp to a value V'.

        Return V' as a result.
        """
        predicate_value = to_bool(evaluate(predicate, env))

        return (evaluate(if_true_exp, env) if predicate_value
                else evaluate(if_false_exp, env))

    def match(exp, first_term):
        return exp[0] == first_term

    # TODO: use table of special forms (?)
    def is_symbol(exp):
        return isinstance(exp, str)

    def is_literal(exp):
        return not isinstance(exp, list)

    def is_let(exp):
        return match(exp, 'let')

    def is_define(exp):
        return match(exp, 'define')

    def is_lambda(exp):
        return match(exp, 'lambda')

    def is_if(exp):
        return match(exp, 'if')

    def is_binding(exp):
        return isinstance(exp, str)

    def function_call(exp):
        function = env.lookup(exp[0])
        args = [evaluate(x, env) for x in exp[1:]]
        return function(*args)

    if not exp:
        return NIL
    elif is_symbol(exp):
        return env.lookup(exp)
    elif is_literal(exp):
        return exp
    elif is_if(exp):
        _, predicate, if_true, if_false = exp
        return if_(predicate, if_true, if_false)
    elif is_let(exp):
        _, bindings, body = exp
        return let(bindings, body)
    elif is_define(exp):
        _, name, exp = exp
        return define(name, exp)
    elif is_lambda(exp):
        _, args, body = exp
        return F(args, body, env)
    else:
        return function_call(exp)


def parse(program):
    """
    Convert string program to an AST.
    """
    tokens = tokenize(program)
    ast = read(tokens)
    return ast


interpreter = compose(parse, evaluate, pretty_print)


if __name__ == '__main__':
    program = sys.argv[-1]
    interpreter(program)
