import ecce.tsk as tsk
import numpy as np
from ecce.constants import *
from ecce.utils import *
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from toolz import memoize
from toolz.curried import map


@memoize
def data_split():
    bow = bag_of_words(tsk.init())
    vectors = pipe(bow, map(second), list, np.array)
    uuids = pipe(bow, map(first), list, np.array, reshape_one_hot_encode,
                 uuid_encoder().transform)
    return train_test_split(vectors, (uuids), test_size=0.2, random_state=1337)

@memoize
def uuid_encoder():
    encoder = OneHotEncoder()

    pipe(tsk.init(),
         bag_of_words,
         map(first),
         list,
         np.array,
         reshape_one_hot_encode,
         encoder.fit_transform)

    return encoder


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
