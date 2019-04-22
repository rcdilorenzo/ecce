import json
import pickle
from multiprocessing import Pool, cpu_count

import ecce.esv
import ecce.passage as passage
import ecce.reference as ref
import ecce.model.nave.data as nave_data
import pandas as pd
import spacy
from ecce.constants import *
from ecce.utils import *
from funcy import first, flatten, memoize, second, rpartial
from lenses import lens
from pymonad.Maybe import *
from toolz.curried import *
from tqdm import tqdm

spacy.prefer_gpu()
# Download with `python -m spacy download en`
nlp = None # Lazy-loaded


@memoize
def init():
    """
    Sample Output:

        [
            ( Reference(book='Exodus', chapter=32, verse=19),
              { 'topic_key': -2146356859,
                'category_key': -2108238392,
                'subtopic_key': 0,
                'subtopic_text': 'General reference(s) to this category',
                'sort_order_subtopic': 0,
                'source_topic_key': '$$T0001327',
                'reference_list': 'Ex32:19,25',
                'topic_name': 'DANCING',
                'category_text': 'Idolatrous',
                'sort_order_category': 3.0 } ),
            ...
        ]

    """
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

def topic_data_frame(module=ecce.esv):
    """Expensive operation to aggregate topics by verse

    (Note: used for export to CSV and then loaded with ecce.model.nave.data)
    """
    columns = ['book', 'chapter', 'verse', 'topics']
    df = pd.DataFrame([
        list(ref._asdict().values()) + [extract_topics_of(data)]
        for (ref, data) in tqdm(init())
    ], columns=columns).groupby(
        ['book', 'chapter', 'verse'],
        as_index=False
    ).aggregate(compose(','.join, set, flatten))

    df['text'] = df.apply(compose(module.text, ref.init_raw_row), axis=1)

    return df


def extract_topics_of(nave_data):
    """Performs NLP on Nave's topics

    Args:
        nave_data (dict): nave subtopic data (see return value of init())

    Returns:
        list of topics
    """
    # TODO: Beef up implementation

    global nlp
    if nlp is None: nlp = spacy.load('en')

    return _extract_topic_name_topics(nave_data['topic_name'])

@memoize
def _extract_topic_name_topics(string):
    if not isinstance(string, str): return []
    if len(string) == 0: return []

    # TODO: Determine how to add this to spaCy pipeline
    string = string.replace('(', '').replace(')', '')

    return [n.text for n in nlp(string).noun_chunks]


def topics_matching_extracted(topic_chunk, references=False):
    """Find all topic-based rows where the label includes the topic_chunk.
    Return data frame with columns (id, label, reference_count, references)
    """
    frame = by_topic_nodes(references=references)
    results = frame[frame.label.str.contains(topic_chunk, regex=False, case=False, na=False)]
    return results.sort_values('reference_count', ascending=False)


def top_topic_matching_extracted(topic_chunk, references=False):
    """Find most frequently occurring topic row where the label includes the
    topic_chunk.

    Return data frame with columns (id, label, reference_count, references)
    """
    results = topics_matching_extracted(topic_chunk)
    if len(results) > 0:
        columns = list(filter(lambda x: x != 'references', results.columns))
        dictionary = json.loads(results.iloc[0][columns].to_json())
        dictionary['references'] = results.iloc[0].references
        return dictionary
    else:
        return None

def by_reference():
    attr = flip(getattr)
    by_book = compose(attr('book'), first)
    by_chapter = compose(attr('chapter'), first)
    by_verse = compose(attr('verse'), first)

    def _to_topics(value):
        return dissoc(
            second(value), 'reference_list', 'source_topic_key',
            'sort_order_category', 'subtopic_key', 'category_key', 'topic_key',
            'sort_order_subtopic')

    return {
        book: {
            chapter: {
                verse: list_map(_to_topics, values)
                for verse, values in groupby(by_verse, chap_values).items()
            }
            for chapter, chap_values in groupby(by_chapter,
                                                book_values).items()
        }
        for book, book_values in groupby(by_book, init()).items()
    }

subtopic_id   = lambda v: f"sbtpc:{v['subtopic_key']}:{v['source_topic_key']}"
subtopic_text = lambda v: v['subtopic_text']
category_id   = lambda v: f"cat:{v['category_key']}"
category_text = lambda v: v['category_text']
topic_id      = lambda v: f"tpc:{v['topic_key']}"
topic_text    = lambda v: v['topic_name']

group_attr = lambda f: compose(f, second, first)

def by_subtopic_nodes():
    attr = flip(getattr)
    by_subtopic = compose(subtopic_id, second)

    return _by_group_transform(by_subtopic, {
        'id': group_attr(subtopic_id),
        'category_id': group_attr(category_id),
        'label': group_attr(subtopic_text),
        'reference_count': len,
        'passages': compose(
            list_map(passage.compact), passage.text, passage.init,
            list_map(first))
    }.items())


def by_category_nodes():
    by_category = compose(category_id, second)

    return _by_group_transform(by_category, {
        'id': group_attr(category_id),
        'topic_id': group_attr(topic_id),
        'label': group_attr(category_text),
        'reference_count': len
    }.items())


@memoize
def by_topic_nodes(references=False):
    """Transform init() frame into the following columns:

        id, label, reference_count, references (optional)
    """
    by_topic = compose(topic_id, second)

    options = {
        'id': group_attr(topic_id),
        'label': group_attr(topic_text),
        'reference_count': len
    }

    if references:
        references_option = {
            'references': compose(list, map(first))
        }
        options = {**options, **references_option}

    return _by_group_transform(by_topic, options.items())


def _by_group_transform(groupby_f, columns_to_transforms):
    attr = flip(getattr)
    category_id = lambda v: v['category_key']
    category_text = lambda v: v['category_text']

    by_category = compose(category_id, second)
    to_data = juxt(list_map(second, columns_to_transforms))

    data = list_map(to_data, groupby(groupby_f, init()).values())

    return pd.DataFrame(data, columns=list_map(first, columns_to_transforms))


def by_topic():
    attr = flip(getattr)
    by_topic = compose(lambda v: v['topic_name'], second)
    by_category = compose(lambda v: v['category_text'], second)
    by_subtopic = compose(lambda v: v['subtopic_text'], second)

    def _to_references(value):
        return dissoc(
            second(value), 'reference_list', 'source_topic_key',
            'sort_order_category', 'subtopic_key', 'category_key', 'topic_key',
            'sort_order_subtopic')

    return {
        topic: {
            category: {
                subtopic: passage.text(passage.init(list_map(first, values)))
                for subtopic, values in groupby(by_subtopic,
                                                chap_values).items()
            }
            for category, chap_values in groupby(by_category,
                                                 topic_values).items()
        }
        for topic, topic_values in groupby(by_topic, init()).items()
    }


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


def parse(raw_reference, abbreviations=NAVE_ABBREVIATIONS):
    def _expand_book(raw):
        """Converts "Lu2:3,4,5" to ("Luke", "2:3,4,5")"""
        return pipe(
            abbreviations.keys(), partial(sorted, key=len), reversed,
            list_filter(lambda k: k in raw), first, to_maybe) >> (
                lambda k: Just((abbreviations[k], raw.replace(k, ''))))

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
            return map(lambda verse: to_maybe(ref.init(book, chapter, verse)),
                       verses)

        return concat(map(_from_chapters, chapters))

    return pipe(
        raw_reference.split('; '),

        # Initial text conversion
        map(
            mconcat_bind([
                _expand_book,
                compose(to_maybe, lens[1].modify(_expand_chapter)),
                compose(to_maybe, lens[1].Each()[1].modify(_expand_verses))
            ])),
        mcompact,

        # Convert data structure to validated ESV references
        map(_to_references),
        flatten,
        mcompact)


def topics_frame(passage_or_passages):
    if isinstance(passage_or_passages, list):
        references = pipe(
            passage_or_passages,
            map(rpartial(getattr, 'references')),
            concat,
            set)
    else:
        references = set(passage_or_passages.references)

    df = by_topic_nodes(references=True)
    overlapping = df.references.apply(lambda r: len(set(r) & references) > 0)

    return df[overlapping]
