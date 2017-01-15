from argparse import ArgumentParser

from .parser import interpreter


parser = ArgumentParser(description='Minimalistic LISP interpreter.')
parser.add_argument('program', type=str)
parser.add_argument('--string', dest='is_from_string', action='store_const',
            const=True, default=False,
            help='Allow to pass string instead of path to file.')

args = parser.parse_args()


if args.is_from_string:
    interpreter(args.program)
else:
    with open(args.program) as program_file:
        interpreter(program_file.read())
