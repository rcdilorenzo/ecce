import ecce.esv as esv
from ecce.utils import *
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from toolz import pipe, memoize


def _bible_text(translation=esv):
    return list_map(lambda r: r[3], translation.flattened_verses())


def vector(text, translation=esv):
    return representation([text], translation=translation)[0]


def representation(text_list, translation=esv):
    """Converts list of sentences to a vocabulary-vectorized, SVD-reduced
    representation
    """
    return pipe(
        text_list,
        vocabulary_vectorizer(translation=translation).transform,
        svd(translation=translation).transform,
    )


@memoize
def svd(n_components=100, translation=esv):
    """Truncated singular value decomposition
    for dimensionality reduction of ESV verses
    """
    svd = TruncatedSVD(n_components=n_components)
    svd.fit(vocabulary_vectorizer().transform(_bible_text(translation)))
    return svd


@memoize
def vocabulary_vectorizer(translation=esv):
    vectorizer = CountVectorizer()
    vectorizer.fit_transform(_bible_text(translation))
    return vectorizer
