import csv
import logging
import sys
import uuid
import warnings
from multiprocessing import Pool, cpu_count

import ecce.modeling.nave.data as data
import ecce.modeling.text as text
import ecce.reference as reference
import pandas as pd
from ecce.constants import *
from ecce.nave import parse as nave_parse
from ecce.utils import *
from funcy import first, second
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
