from multiprocessing import Pool, cpu_count

import pandas as pd
import pickle
from funcy import first, flatten
from lenses import lens
from pymonad.Maybe import *
from toolz.curried import *
from tqdm import tqdm

import ecce.reference as ref
from ecce.constants import *
from ecce.utils import *


@memoize
def init():
    if os.path.isfile(NAVE_PATH):
        with open(NAVE_PATH, 'rb') as f:
            return pickle.load(f)

    iterator = tqdm(df().iterrows(), total=len(df()))

    print('Parsing all references...')

    pool = Pool(cpu_count())
    results = list(concat(pool.map(_parse_refs, iterator)))

    with open(NAVE_PATH, 'wb') as f:
        pickle.dump(results, f)

    return results


@memoize
def df():
    if os.path.isfile(NAVE_FRAME_PATH):
        return pd.read_csv(NAVE_FRAME_PATH)

    categories = pd.read_csv(
        NAVE_CAT_PATH,
        sep='\t',
        names=[
            'topic_key', 'category_key', 'category_text', 'sort_order',
            'source_topic_key'
        ])

    topics = pd.read_csv(
        NAVE_TOPIC_PATH,
        sep='\t',
        names=['topic_key', 'topic_name', 'source_topic_key'])

    subtopics = pd.read_csv(
        NAVE_SUBTOPIC_PATH,
        sep='\t',
        names=[
            'topic_key', 'category_key', 'subtopic_key', 'subtopic_text',
            'sort_order', 'source_topic_key', 'reference_list'
        ])

    df = pd.merge(
        subtopics,
        pd.merge(
            topics,
            categories,
            on=['topic_key', 'source_topic_key'],
            how='left'),
        on=['topic_key', 'source_topic_key', 'category_key'],
        how='left',
        suffixes=('_subtopic', '_category'))

    df.to_csv(NAVE_FRAME_PATH, index=False)
    return df


def _parse_refs(index_and_row):
    _, row = index_and_row
    return list_map(lambda reference: (reference, row.to_dict()),
                    parse(row.at['reference_list']))


def parse(raw_reference):
    def _expand_book(raw):
        """Converts "Lu2:3,4,5" to ("Luke", "2:3,4,5")"""
        return pipe(
            NAVE_ABBREVIATIONS.keys(),
            partial(sorted, key=len),
            reversed,
            list_filter(lambda k: k in raw),
            first,
            to_maybe
        ) >> (lambda k: Just((NAVE_ABBREVIATIONS[k], raw.replace(k, ''))))

    def _expand_chapter(raw):
        """Converts "2:3,4,5" to (2, "3, 4, 5")"""
        # Fix data misformat
        raw = raw.replace('-626:', '-6,26:')

        if raw.count(':') > 1:
            return list(concat(map(_expand_chapter, raw.split(','))))
        else:
            chapter, verses = raw.split(':')
            return [(int(chapter), verses)]

    def _expand_verses(raw):
        """Converts "3,4,5" or "3-5" to [3, 4, 5]"""
        if ',' in raw:
            return list(flatten(map(_expand_verses, raw.split(','))))
        elif '-' in raw:
            components = list_map(int, raw.split('-'))
            return list(range(components[0], components[-1] + 1))
        else:
            return [int(raw)]

    def _to_references(data):
        """Converts ('Luke', [(2, [3, 4, 5]), ...]) to (List ref.Data)"""
        book, chapters = data

        def _from_chapters(pair):
            chapter, verses = pair
            return map(
                lambda verse: to_maybe(ref.init(book, chapter, verse)),
                verses)

        return concat(map(_from_chapters, chapters))

    return pipe(
        raw_reference.split('; '),

        # Initial text conversion
        map(mconcat_bind([
            to_maybe, _expand_book,
            compose(to_maybe, lens[1].modify(_expand_chapter)),
            compose(to_maybe, lens[1].Each()[1].modify(_expand_verses))
        ])),
        mcompact,

        # Convert data structure to validated ESV references
        map(_to_references),
        flatten,
        mcompact
    )
