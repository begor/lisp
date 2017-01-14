import functools
import operator


class Env(dict):
    """TODO: tests"""

    def __init__(self, names=(), values=(), outer=None):
        self.update(zip(names, values))
        self.outer = outer

    def lookup(self, name):
        "Find the innermost Env where var appears."
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
        'cons': lambda x, thelist: [x] + thelist,
        'list': lambda *xs: list(xs),
        'car': lambda alist: alist[0],
        'cdr': lambda alist: alist[1:],
        'valof': lambda name: env[name],
    })

    return env

default = builtins()
