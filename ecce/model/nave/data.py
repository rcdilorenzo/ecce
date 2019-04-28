import logging

import ecce.model.text as text
import pandas as pd
from ascii_graph import Pyasciigraph
from ecce.constants import *
from ecce.utils import cache_frame
from funcy import flatten
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from toolz import memoize
from tqdm import tqdm

EXCLUDED_TOPICS = set(['JESUS', 'THE CHRIST', 'GOD'])

@memoize
def frame():
    def _split_topics(topics):
        if not isinstance(topics, str): return []
        return topics.split(',')

    df = pd.read_csv(NLP_TOPICS_PATH, sep='\t')
    df.topics = df.topics.apply(_split_topics)

    clause = df.topics.apply(len) != 0
    clause_counts = clause.value_counts()
    if False in clause_counts.index:
        count = clause_counts.loc[False]
        logging.warning(f'Skipping {count} verses with no assigned topics.')

    return df[clause]


@memoize
def filtered_frame(min_per_topic=MIN_VERSES_PER_TOPIC):
    df = frame().copy()
    counts_df = verse_counts()
    whitelist_topics = set(counts_df.topic_name[
        counts_df.verse_count >= min_per_topic].values) - EXCLUDED_TOPICS
    df.topics = df.topics.apply(lambda topics: list(
        filter(lambda t: t in whitelist_topics, topics)))
    return df[df.topics.apply(len) > 0]


def tokenize(sentences):
    return text.representation(sentences, include_svd=False)


@memoize
def topic_chunk_encoder(min_per_topic=MIN_VERSES_PER_TOPIC):
    encoder = MultiLabelBinarizer()
    encoder.fit_transform(filtered_frame(min_per_topic).topics.values)
    return encoder


@memoize
def data_split(min_per_topic=MIN_VERSES_PER_TOPIC):
    df = filtered_frame(min_per_topic)
    text = tokenize(df.text.values)
    topics = topic_chunk_encoder().transform(df.topics.values)
    return train_test_split(text, topics, test_size=0.2, random_state=1337)


@cache_frame(CACHE_VERSE_COUNTS)
def verse_counts():
    topics = frame().topics
    counts_by_topic = [(t, topics.apply(lambda values: t in values).sum())
                       for t in tqdm(set(flatten(topics.values)))]
    return pd.DataFrame(counts_by_topic, columns=['topic_name', 'verse_count'])


@memoize
def topic_counts():
    df = frame()
    verse = df.apply(
        lambda r: f"{r.at['book']} {r.at['chapter']}:{r.at['verse']}", axis=1)
    topic_count = df.topics.apply(len)
    return pd.DataFrame(dict(verse=verse, topic_count=topic_count))


def topic_histogram():
    df = frame().topics.apply(len).value_counts().sort_index()
    return [(f'{count} topic{"" if count == 1 else "s"}', freq)
            for count, freq in zip(df.index, df.values)]


def print_topic_graph():
    graph = Pyasciigraph(line_length=40)
    [print(l) for l in graph.graph('# Topics per Verse', topic_histogram())]
