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


def parse(program):
    tokens = tokenize(program)
    print(tokens)
    ast = read(tokens)
    print(ast)

if __name__ == '__main__':
    parse('(+ 2 (- 4 (* 2 1)))')
