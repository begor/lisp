from functools import reduce

from lisp.environment import default, Env


NIL = []


def procedure(params, body, env):
    """
    User defined procedure.

    Uses lexical scoping (lookup names in the place it was defined).
    """
    return lambda *args: evaluate_expression(body, Env(params, args, env))


def to_bool(value):
    """Convert arbitary value to boolean."""
    falsy = ['false', [], 0]

    return False if value in falsy else True


def evaluate_expression(exp, env=default):
    """
    Evaluate expression exp in environment env.

    Expression represented as a list of terms.
    Environment as an instance of Env class.

    Example:
    > evaluate_expression([+, 2, [-, 4, 2]], Env())  # Passing empty env
    >> 4
    """

    def function_call(exp):
        """
        Handle function call.

        In lisp every s-expression is a function-call.
        First element is a function name (or a function itself).
        Other elements are argumets to that function.
        """
        func, *args = exp
        function_to_call = evaluate_expression(func, env)
        args = [evaluate_expression(x, env) for x in args]
        return function_to_call(*args)

    def let(bindings, body):
        """
        Handle let special form.

        First, extend current environment with bindings.
        Second, evaluate body under extended environment.
        """
        names = [b[0] for b in bindings]
        values = [evaluate_expression(b[1], env) for b in bindings]
        new_env = Env(names=names, values=values, outer=env)
        return evaluate_expression(body, new_env)

    def define(name, exp):
        """
        Handle define special form.

        First, evaluate exp under under current environment to a value V.
        Second, extend current environment with name -> V pair.

        Return V as a result.
        """
        val = evaluate_expression(exp, env)
        env.update({name: val})
        return val

    def if_(predicate, if_true_exp, if_false_exp):
        """
        Handle if special form.

        First, evaluate predicate under current environment to a value V.
        Second, if V is truthy evaluate if_true_exp to a value V'.
        Otherwise, evaluate if_false_exp to a value V'.

        Return V' as a result.
        """
        predicate_value = to_bool(evaluate_expression(predicate, env))

        return (evaluate_expression(if_true_exp, env) if predicate_value
                else evaluate_expression(if_false_exp, env))

    def set_(name, exp):
        """
        Handle 'set!' special form.

        If name exists in current environment, update its value.
        Else, fail.

        Note: works ONLY for symbols/name/envs. Lists are immutable.
        """
        value = evaluate_expression(exp, env)
        env.set(name, value)
        return value

    def quasiquoute(exp):
        """
        Handle 'quasiquoute' special form.

        Traverse given exp, if subexpression is 'unquote' special form,
        evaluate it. If not -- left as is.

        Return modified exp.
        """
        return [evaluate_expression(datum, env) if is_unquote(datum) else datum
                for datum in exp]

    def match(exp, first_term):
        return isinstance(exp, list) and exp[0] == first_term

    def is_symbol(exp):
        return isinstance(exp, str)

    def is_literal(exp):
        return not isinstance(exp, list)

    def is_let(exp):
        return match(exp, 'let')

    def is_quasiqoute(exp):
        return match(exp, 'quasiquote')

    def is_quote(exp):
        return match(exp, 'quote')

    def is_unquote(exp):
        return match(exp, 'unquote')

    def is_define(exp):
        return match(exp, 'define')

    def is_lambda(exp):
        return match(exp, 'lambda')

    def is_if(exp):
        return match(exp, 'if')

    def is_set(exp):
        return match(exp, 'set!')

    # Kinda of pattern-matching.
    if not exp:
        return NIL
    elif is_symbol(exp):
        return env.lookup(exp)
    elif is_literal(exp):
        return exp
    elif is_quote(exp):
        _, datum = exp
        return datum
    elif is_unquote(exp):
        _, datum = exp
        return evaluate_expression(datum, env)
    elif is_quasiqoute(exp):
        _, datum = exp
        return quasiquoute(datum)
    elif is_if(exp):
        _, predicate, true_branch, false_branch = exp
        return if_(predicate, true_branch, false_branch)
    elif is_let(exp):
        _, bindings, body = exp
        return let(bindings, body)
    elif is_set(exp):
        _, name, value = exp
        return set_(name, value)
    elif is_define(exp):
        _, name, exp = exp
        return define(name, exp)
    elif is_lambda(exp):
        _, args, body = exp
        return procedure(args, body, env)
    else:
        return function_call(exp)
