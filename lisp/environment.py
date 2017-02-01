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

    lookup_error_msg = '{} not found in Env{}'

    def __init__(self, names=(), values=(), outer=None):
        self.update(zip(names, values))
        self.outer = outer

    def set(self, name, new_value):
        self.lookup(name)  # Will fail if no name in Env
        self[name] = new_value

    def lookup(self, name):
        if name in self:
            return self[name]
        elif self.outer:
            return self.outer.lookup(name)
        else:
            raise LookupError(self.lookup_error_msg.format(name, self))



def builtins():
    """
    Define default environment full of builtin procedures.

    Basic primitives which all Lisps should have:
        eq?
        quote
        cons
        car
        cdr
        atom?

    In addition, this Lisp also have:
    - a set of numeric operations (+, -, =, /, etc)
    - reflection functions (list?, number?, symbol?, etc)
    - list processing functions (map, filter, foldl, etc) # TODO
    """
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
