import logging
import os

import numpy as np
import pandas as pd
from ascii_graph import Pyasciigraph
from funcy import flatten
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer, text_to_word_sequence
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from toolz import compose, memoize, partial, pipe
from tqdm import tqdm

from ecce.constants import GLOVE_PATH, GLOVE_WORD2VEC_PATH, NLP_TOPICS_PATH, WORD_EMBEDDINGS


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
def _text_tokenizer():
    """Text tokenizer to convert verses (sentences) to numerical sequences

    (Note: Intended use is within data.tokenize)

    Usage:
        >>> t = data._text_tokenizer()
        >>> t.texts_to_sequences(['this is a test.'])
        [[41, 14, 9]]
    """
    max_length = frame().text.apply(compose(len, text_to_word_sequence)).max()
    tokenizer = Tokenizer(num_words=max_length)
    tokenizer.fit_on_texts(preprocess_text(frame().text.values))
    return tokenizer


def preprocess_text(sentences):
    "Remove apostrophes to match more word embeddings from GloVe"
    return map(lambda s: s.replace("'s ", ' ').replace("'", ''), sentences)


@memoize
def gensim_model():
    "Load GloVe embeddings into a gensim model"
    if not os.path.isfile(GLOVE_PATH):
        logging.error(
            f'No GloVe file found ({GLOVE_PATH}). Please run download.sh to install.'
        )
        exit()

    if not os.path.isfile(GLOVE_WORD2VEC_PATH):
        logging.info('Converting GloVe file to word2vec...')
        glove2word2vec(GLOVE_PATH, GLOVE_WORD2VEC_PATH)

    return KeyedVectors.load_word2vec_format(GLOVE_WORD2VEC_PATH)


@memoize
def embedding_matrix():
    "Generate 100-dimensional word vectors from Bible words using GloVe"
    if os.path.isfile(WORD_EMBEDDINGS):
        return np.load(WORD_EMBEDDINGS, allow_pickle=False)

    logging.info('Loading embedding matrix...')
    model = gensim_model()
    tokenizer = _text_tokenizer()

    # zero has all zero weights
    word_count = len(tokenizer.word_index) + 1
    vector_size = model.vector_size

    matrix = np.zeros((word_count, vector_size))
    missing_words = []
    for word, index in tokenizer.word_index.items():
        try:
            matrix[index] = model.word_vec(word)
        except KeyError as e:
            missing_words.append(word)

    if len(missing_words) > 0:
        values = np.array(missing_words)
        count = len(missing_words)
        stats = f'{count} / {word_count} ({(100 * count / word_count):.2f}%)'
        logging.warning(
            f'{stats} not found in word embeddings:\n{values}'
        )

    with open(WORD_EMBEDDINGS, 'wb') as f:
        logging.debug(f'Saving word embeddings to "{WORD_EMBEDDINGS}"...')
        np.save(f, matrix, allow_pickle=False)

    return matrix


def tokenize(sentences):
    """Tokenize sentences into a (sentence count, max length) matrix

    Usage:
        >>> data.tokenize(['this is a test.', 'God is good.'])
        array([[41, 14,  9,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
               [31, 14,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]],
               dtype=int32)
    """
    tokenizer = _text_tokenizer()

    return pipe(
        sentences,
        preprocess_text,
        tokenizer.texts_to_sequences,
        partial(pad_sequences, maxlen=tokenizer.num_words, padding='post'))


@memoize
def vocabulary_vectorizer():
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
    text = tokenize(df.text.values)
    topics = topic_encoder().transform(df.topics.values)
    return train_test_split(text, topics, test_size=0.2, random_state=1337)


def topic_histogram():
    topic_counts = frame().topics.apply(len).value_counts().sort_index()
    return [(f'{count} topic{"" if count == 1 else "s"}', freq)
            for count, freq in zip(topic_counts.index, topic_counts.values)]


def print_topic_graph():
    graph = Pyasciigraph(line_length=40)
    [print(l) for l in graph.graph('# Topics per Verse', topic_histogram())]
