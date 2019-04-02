import logging

import pandas as pd
from ascii_graph import Pyasciigraph
from funcy import flatten
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from toolz import memoize

from ecce.constants import NLP_TOPICS_PATH


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
def text_vectorizer():
    vectorizer = CountVectorizer()
    vectorizer.fit_transform(frame().text.values)
    return vectorizer


@memoize
def topic_encoder():
    encoder = MultiLabelBinarizer()
    encoder.fit_transform(frame().topics.values)
    return encoder


@memoize
def data_split():
    df = frame()
    text = df.text.values
    topics = topic_encoder().transform(df.topics.values)
    return train_test_split(text, topics, test_size=0.25, random_state=1337)


def topic_histogram():
    topic_counts = frame().topics.apply(len).value_counts().sort_index()
    return [(f'{count} topic{"" if count == 1 else "s"}', freq)
            for count, freq in zip(topic_counts.index, topic_counts.values)]


def print_topic_graph():
    graph = Pyasciigraph(line_length=40)
    [print(l) for l in graph.graph('# Topics per Verse', topic_histogram())]
