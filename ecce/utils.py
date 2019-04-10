import hashlib
import os
import logging
import pandas as pd
from functools import reduce

from pymonad.List import *
from pymonad.Maybe import *
from toolz.curried import *

list_filter = curry(lambda f, x: list(filter(f, x)))
list_map = curry(lambda f, x: list(map(f, x)))
lines = '\n'.join

def cache_frame(filename, tsv=False):
    def decorator(f):
        def wrapped_f(*args):
            call_filename = filename.format(
                hashlib.md5(str(args).encode('utf-8')).hexdigest()[0:6]
            )
            if os.path.isfile(call_filename) is False:
                df = f(*args)
                logging.info(f'Saving to {call_filename}...')
                df.to_csv(call_filename, sep=('\t' if tsv else ','), index=False)
                return df

            return pd.read_csv(call_filename)
        return wrapped_f
    return decorator


def relative_path(current_file, path):
    return os.path.join(os.path.dirname(current_file), path)


def to_maybe(value):
    """Implementation of a -> Maybe a"""
    return Just(value) if value else Nothing


def mcompact(list_of_maybes):
    """Implementation of concat [Monoid a] -> [a]"""
    return pipe(list_of_maybes,
                filter(lambda x: x is not mzero(x.__class__)),
                map(lambda x: x.getValue()),
                list)


def mconcat_bind(list_of_monadic_binds):
    """Implementation of List (a -> Monad a) -> (a -> Monad a)"""
    return reduce(lambda left, right: (lambda x: left(x) >> right),
                  list_of_monadic_binds)
