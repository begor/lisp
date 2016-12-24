def tokenize(program):
    """
    I: (+ 2 (- 4 2))
    O: [(, +, 2, (, -, 4, 2, ), )]
    """
    return program.replace(')', ' ) ').replace('(', ' ( ').split()

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
        return t


def evaluate(exp):
    """
    I: [+, 2, [-, 4, 2]]
    O: 4
    """
    operations = {
        '+': lambda x, y: evaluate(x) + evaluate(y),
        '-': lambda x, y: evaluate(x) - evaluate(y),
        '*': lambda x, y: evaluate(x) * evaluate(y),
        '/': lambda x, y: evaluate(x) / evaluate(y),
    }

    def function_call(function, *args):
        return function(*args)

    def atom(exp):
        try:
            return int(exp)
        except ValueError:
            try:
                return float(exp)
            except ValueError:
                return exp


    if exp[0] in operations:
        return function_call(operations[exp[0]], exp[1], exp[2])
    else:
        return atom(exp)

def parse(program):
    tokens = tokenize(program)
    ast = read(tokens)
    return ast

if __name__ == '__main__':
    ast = parse('(+ 2 (- 4 (* 2 1)))')
    print(evaluate(ast))
