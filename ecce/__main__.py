import argparse
import sys

from ecce.cli import *
from toolz import pipe


def add_nave_export(subparsers):
    parser = subparsers.add_parser(
        'nave-export', help='Export processed data from Nave\'s Topical Index')
    parser.set_defaults(func=export_nave)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    pipe(parser.add_subparsers(), add_nave_export)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
