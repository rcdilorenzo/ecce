import os
from toolz.curried import *
from functools import reduce
from pymonad.Maybe import *
from pymonad.List import *


list_filter = curry(lambda f, x: list(filter(f, x)))
list_map = curry(lambda f, x: list(map(f, x)))

def relative_path(current_file, path):
    return os.path.join(os.path.dirname(current_file), path)

def to_maybe(value):
    """Implementation of a -> Maybe a"""
    return Just(value) if value else Nothing

def mcompact(list_of_maybes):
    """Implementation of concat [Monoid a] -> [a]"""
    return pipe(
        list_of_maybes,
        filter(lambda x: x is not mzero(x.__class__)),
        map(lambda x: x.getValue()),
        list
    )

def mconcat_bind(list_of_monadic_binds):
    """Implementation of List (a -> Monad a) -> (a -> Monad a)"""
    return reduce(
        lambda left, right: (lambda x: left(x) >> right),
        list_of_monadic_binds
    )
