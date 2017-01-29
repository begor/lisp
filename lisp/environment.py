import functools
import operator


class Env(dict):
    """
    Environment for some computation.

    Implemented with recursive composition -
    each environment has the outer environment.
    Every lookup for a name N in the environment E
    with outer environment O goes like this:

    1) E.lookup(N)
    2) O.lookup(N)
    3) O.O.lookup(N)
    ...

    Until we find N in some environment.
    """

    def __init__(self, names=(), values=(), outer=None):
        self.update(zip(names, values))
        self.outer = outer

    def lookup(self, name):
        # TODO: use magic method instead
        return self[name] if (name in self) else self.outer.lookup(name)



def builtins():
    env = Env()
    env.update({
        '+': lambda *args: sum(args),
        '*': lambda *args: functools.reduce(operator.mul, args),
        '-': operator.sub,
        '/': operator.truediv,
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '=': operator.eq,
        'and': operator.and_,
        'or': operator.or_,
        'car': lambda alist: alist[0],
        'cdr': lambda alist: alist[1:],
        'cons': lambda head, tail: [head] + tail,
        'list': lambda *terms: list(terms),
        'sum': sum,
        'list?': lambda term: isinstance(term, list),
        'atom?': lambda term: isinstance(term, (int, float, str)),
        'number?': lambda term: isinstance(term, (int, float)),
        'symbol?': lambda term: isinstance(term, str),
        'function?': callable,
        'eq?': operator.eq,
    })

    return env

default = builtins()
