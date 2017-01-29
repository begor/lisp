import functools
import sys


def tokenize(program):
    """
    Convert string to a list of tokens.

    Example:
    > (+ 2 (- 4 2))
    > [(, +, 2, (, -, 4, 2, ), )]
    """
    one_liner = program.replace('\n', '')
    program = one_liner.replace(')', ' ) ').replace('(', ' ( ')
    ololo = program.split()
    print(ololo)
    return ololo


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
    Read list tokens, return AST.

    Tokens represented as a flat list.
    AST represented as a nested lists.

    Exaple:
    > read([(, +, 2, (, -, 4, 2, ), )])
    >> [+, 2, [-, 4, 2]]
    """

    if not len(tokens):
        raise SyntaxError('Empty program')

    # TODO: rewrite entirely!
    ast = []
    deep = 0
    current = prev = ast
    stack = []  # Stack of nested nodes (TODO: looks wierd)
    for i, t in enumerate(tokens):
        if t == '(':
            deep += 1
            new_current = []
            current.append(new_current)
            stack.append(current)
            current = new_current
        elif t == ')':
            if deep == 0:
                raise SyntaxError('Unexpected ) term')
            else:
                deep -= 1
                current = stack.pop()
        else:
            current.append(atomize(t))

    if deep > 0:
        raise SyntaxError('Missing ) term')

    return ast


def parse(program):
    """Convert string program to an AST."""
    tokens = tokenize(program)
    ast = read(tokens)
    return ast
