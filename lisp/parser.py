import operator
import functools
import sys

DEFAULT_ENV = {
    '+': lambda *args: sum(args),
    '*': lambda *args: functools.reduce(operator.mul, args),
    '-': operator.sub,
    '/': operator.truediv,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '=': operator.eq,
    'cons': lambda *args: list(args),
    'car': lambda alist: alist[0],
    'cdr': lambda alist: alist[1],
    'valof': lambda name: env[name]
}


def compose(*fs):
    def compose2(f, g):
        return lambda *a, **kw: f(g(*a, **kw))
    return functools.reduce(compose2, reversed(fs))


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
    I: [(, +, 2, (, -, 4, 2, ), )]
    O: [+, 2, [-, 4, 2]]
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
        raise SyntaxError()
    else:
        return atomize(t)


def evaluate(exp, env=dict(DEFAULT_ENV)):
    """
    I: [+, 2, [-, 4, 2]]
    O: 4
    """
    def let_expression(bindings, exp):
        for name, value in bindings:
            env[name] = evaluate(value, env)
        return evaluate(exp, env)

    def is_funcall(exp):
        return isinstance(exp, list) and exp[0] in env

    def is_let(exp):
        return isinstance(exp, list) and exp[0] == 'let'

    def is_binding(exp):
        return isinstance(exp, str)

    def is_define(exp):
        return isinstance(exp, list) and exp[0] == 'define'

    def function_call(exp):
        function = env[exp[0]]
        args = [evaluate(x, env) for x in exp[1:]]
        return function(*args)

    if not exp:
        return []
    elif is_let(exp):
        return let_expression(*exp[1:])
    elif is_define(exp):
        _, name, value = exp
        val = evaluate(value, env)
        env[name] = val
        return val
    elif is_funcall(exp):
        return function_call(exp)
    elif is_binding(exp):
        return env[exp]
    else:
        return exp


def parse(program):
    tokens = tokenize(program)
    ast = read(tokens)
    return ast


pretty_print = print


interpreter = compose(parse, evaluate, pretty_print)


if __name__ == '__main__':
    program = sys.argv[-1]
    interpreter(program)
