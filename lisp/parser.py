import operator
from functools import reduce


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


def evaluate(exp):
    """
    I: [+, 2, [-, 4, 2]]
    O: 4
    """
    operations = {
        '+': lambda *args: sum(args),
        '-': operator.sub,
        '*': lambda *args: reduce(operator.mul, args),
        '/': operator.truediv,
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '=': operator.eq,
    }

    def is_operation(exp):
        return isinstance(exp, list) and exp[0] in operations

    def function_call(exp):
        function = operations[exp[0]]
        args = [evaluate(x) for x in exp[1:]]
        return function(*args)

    if not exp:
        return
    if is_operation(exp):
        return function_call(exp)
    else:
        return exp


def parse(program):
    tokens = tokenize(program)
    ast = read(tokens)
    return ast

if __name__ == '__main__':
    ast = parse('(+ 2 (- 4 (* 2 1)))')
    print(evaluate(ast))
