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
        'train-lstm', help='Train an LSTM neural network model on Nave data')
    parser.add_argument('-e', '--epochs', type=int, default=20)
    parser.add_argument('-p', '--patience', type=int, default=3)
    parser.set_defaults(func=train_lstm)

    parser = subparsers.add_parser('train-gru', help='Train a GRU model on Nave data')
    parser.add_argument('-e', '--epochs', type=int, default=20)
    parser.add_argument('-p', '--patience', type=int, default=3)
    parser.set_defaults(func=train_gru)

    parser = subparsers.add_parser('train-tsk', help='Train cluster model on TSK data')
    parser.add_argument('-e', '--epochs', type=int, default=20)
    parser.add_argument('-p', '--patience', type=int, default=3)
    parser.set_defaults(func=train_tsk_clusters)
    return subparsers


def add_predict(subparsers):
    parser = subparsers.add_parser(
        'predict-lstm', help='(REPL) Predict topics based on text')
    parser.add_argument('-w', '--weights', type=str)
    parser.add_argument('-t', '--threshold',
                        type=float,
                        default=0.5,
                        help='Threshold for topic probability')
    parser.set_defaults(func=predict_lstm)
    return subparsers


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    pipe(
        parser.add_subparsers(),
        add_nave_export,
        add_topics_export,
        add_train,
        add_predict
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
