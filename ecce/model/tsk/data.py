from multiprocessing import Pool, cpu_count

import ecce.model.text as text
import ecce.tsk as tsk
import ecce.esv as esv
import numpy as np
from ecce.constants import *
from ecce.utils import *
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from toolz import memoize
from toolz.curried import map
from tqdm import tqdm


@memoize
def data_split():
    # TODO: Use word embeddings instead of SVD for words in order to better
    # generalize when unfamiliar words are used

    bow = bag_of_words(tsk.flattened_uuids())
    vectors = pipe(bow, map(second), list, np.array)
    uuids = pipe(bow, map(first), list, np.array,
                 uuid_encoder().transform)
    return train_test_split(vectors, (uuids), test_size=0.2, random_state=1337)


@memoize
def uuid_encoder():
    encoder = MultiLabelBinarizer(sparse_output=True)
    encoder.fit_transform(tsk.flattened_uuids().uuid.values)
    return encoder


def tokenize(text_lists):
    return pipe(text_lists, map(text.vector), list, np.array)


@cache_pickle(CACHE_TSK_CLUSTERS)
def bag_of_words(frame):
    """Converts a data frame of the following columns

        uuid, phrase, book, chapter, verse

    to a list of SVD-reduced components with the uuid clusters

        [ (['84faacdd'], np.array([ 2.64889813, ... ])),
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
