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
    tokens = one_liner.replace(')', ' ) ').replace('(', ' ( ').split()
    return tokens


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

    current_node = AST = []
    deep = 0
    stack_of_nodes = []
    for t in tokens:
        if t == '(':
            deep += 1
            child_node = []
            current_node.append(child_node)
            stack_of_nodes.append(current_node)
            current_node = child_node
        elif t == ')':
            if deep == 0:
                raise SyntaxError('Unexpected ) term')
            else:
                deep -= 1
                current_node = stack_of_nodes.pop()
        else:
            current_node.append(atomize(t))

    if deep > 0:
        raise SyntaxError('Missing ) term')

    return AST


def parse(program):
    """Convert string program to an AST."""
    tokens = tokenize(program)
    ast = read(tokens)

    return ast
