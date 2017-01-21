import functools
import sys


def tokenize(program):
    """
    Convert string to a list of tokens.

    Example:
    > (+ 2 (- 4 2))
    > [(, +, 2, (, -, 4, 2, ), )]
    """

    return program.replace(')', ' ) ').replace('(', ' ( ').split()


def atomize(token):
    """Try to convert token to numeric literal."""

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


def parse(program):
    """Convert string program to an AST."""
    tokens = tokenize(program)
    ast = read(tokens)
    return ast
