import csv
import logging
import sys
import uuid
import warnings
from multiprocessing import Pool, cpu_count

import ecce.esv as esv
import ecce.modeling.data as data
import ecce.modeling.text as text
import ecce.reference as reference
import numpy as np
import pandas as pd
from ecce.constants import *
from ecce.nave import parse as nave_parse
from ecce.utils import *
from funcy import first, second
from sklearn.model_selection import train_test_split
from toolz import curry, memoize
from tqdm import tqdm

_writer = None


def init():
    if os.path.isfile(TSK_PATH):
        return pd.read_csv(TSK_PATH)

    with open(TSK_PATH, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            'uuid', 'linked_book', 'linked_chapter', 'linked_verse', 'phrase',
            'book', 'chapter', 'verse'
        ])

    iterator = tqdm(df().iterrows(), total=len(df()))

    print('Parsing all references...')

    pool = Pool(cpu_count())
    pool.imap_unordered(_parse_refs(TSK_PATH), iterator)

    return _init()


@memoize
def _init():
    return pd.read_csv(TSK_PATH)


@memoize
def df():
    df = pd.read_csv(
        TSK_RAW_PATH,
        sep='\t',
        encoding='unicode_escape',
        names=[
            'book', 'chapter', 'verse', 'sort_order', 'phrase',
            'reference_list'
        ])

    # Replace book index with actual book name
    df.book = df.book.apply(lambda index: CANONICAL_ORDER[index - 1])

    return df

@memoize
def data_split():
    bow = bag_of_words(init())
    vectors = np.array(map(second, bow))
    uuids = np.array(map(first, bow))
    return train_test_split(vectors, uuids, test_size=0.2, random_state=1337)


@cache_pickle(CACHE_TSK_CLUSTERS)
def bag_of_words(frame):
    """Converts a data frame of the following columns

        uuid, linked_book, linked_chapter, linked_verse, phrase, book, chapter, verse

    to a list of SVD-reduced components with the uuid clusters

        [ ('84faacdd', np.array([ 2.64889813, ... ])),
          ... ]
    """
    iterator = tqdm(frame.iterrows(), total=len(frame))

    print('Cluster bag-of-words SVD reduction...')

    pool = Pool(cpu_count())
    return [r for r in pool.imap_unordered(_bag_of_words, iterator)]


@curry
def _bag_of_words(index_and_row):
    _, row = index_and_row
    return (row.at['uuid'], pipe(row, esv.text, text.vector))


@curry
def _parse_refs(file_path, index_and_row):
    global _writer
    _, row = index_and_row

    data = [
        uuid.uuid4().hex[0:8],
        row.at['book'],
        row.at['chapter'],
        row.at['verse'],
        row.at['phrase'],
    ]

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')

        rows = list_map(
            lambda reference: data + list(ecce.reference.compact(reference)),
            parse(row.at['reference_list']))

    if _writer is None:
        f = open(file_path, 'a')
        _writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        _writer.writerows(rows)
    else:
        _writer.writerows(rows)


def parse(reference_list):
    return nave_parse(
        reference_list
        .replace('so in:;', '')
        .replace('12,1-13', '12:1-13')
        .replace(';', '; '),
        abbreviations=TSK_ABBREVIATIONS)
