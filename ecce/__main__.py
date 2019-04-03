import argparse
import sys

from ecce.cli import *
from toolz import pipe


def add_nave_export(subparsers):
    parser = subparsers.add_parser(
        'nave-export', help='Export processed data from Nave\'s Topical Index')
    parser.set_defaults(func=export_nave)
    return subparsers


def add_topics_export(subparsers):
    parser = subparsers.add_parser(
        'topic-export', help='Preprocess topics and export with ESV text')
    parser.set_defaults(func=export_topics)
    return subparsers


def add_train(subparsers):
    parser = subparsers.add_parser(
        'train-lstm', help='Train an LSTM neural network model')
    parser.set_defaults(func=train_lstm)
    return subparsers


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    pipe(
        parser.add_subparsers(),
        add_train,
        add_nave_export,
        add_topics_export
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
