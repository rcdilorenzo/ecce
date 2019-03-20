from collections import namedtuple as Struct
from toolz.curried import *
from funcy import first
from ecce.utils import *
import ecce.reference as reference

Data = Struct('Passage', ['name', 'references'])

def init(references):
    verse = flip(getattr)('verse')

    def _verses(numbers):
        def _to_string(sequential):
            if len(sequential) == 1:
                return str(first(sequential))
            else:
                return f'{sequential[0]}-{sequential[-1]}'

        def _reduce_verse(acc, number):
            if len(acc) == 0 or len(acc[0]) == 0 or acc[0][-1] != (number - 1):
                return acc + [[number]]
            else:
                return acc[0:-1] + [acc[-1] + [number]]

        return pipe(reduce(_reduce_verse, sorted(numbers), []),
                    map(_to_string),
                    ','.join)

    grouped = groupby(lambda r: (r.book, r.chapter),
                      reference.ordered(references))

    return [Data(f'{k[0]} {k[1]}:{_verses(list_map(verse, references))}',
                      reference.ordered(references))
            for k, references in grouped.items()]
