import os
from argparse import ArgumentParser

from lisp.parser import interpreter


def get_args():
    """Parse CLI arguments, provide help information if needed."""

    parser = ArgumentParser(description='Minimalistic LISP interpreter.')
    parser.add_argument('program', nargs='?', type=str, default=None)
    args = parser.parse_args()
    return str(args.program)


def run_repl():
    """Run lisp REPL."""

    while True:
        interpreter(input('(lisp)> '))


def interpret_from_file(file):
    """Open and read file, interpret its contents."""

    with open(file) as fd:
        interpreter(fd.read())


def eval_(input_):
    """
    Evaluate given input.

    Three cases:
    1) No input -> run REPL
    2) Input is a filepath -> read it and interpret
    3) Input is a arbitary string -> interpret
    """

    is_filepath = lambda: os.path.exists(input_)
    should_run_repl = lambda: input_ is None

    if should_run_repl():
        run_repl()
    elif is_filepath():
        interpret_from_file(input_)
    else:
        interpreter(input_)

eval_(get_args())
