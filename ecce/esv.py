from ecce.constants import ESV_PATH

import json
import logging
from toolz import memoize, concat


@memoize
def verses():
    with open(ESV_PATH) as f:
        logging.info('Loading ESV JSON...')
        return json.load(f)


def flattened_verses():
    return concat(
        concat([[[(book, chapter, verse, content)
                  for verse, content in verses.items()]
                 for chapter, verses in chapters.items()]
                for book, chapters in verses().items()]))


def text(ref):
    return verses()[ref.book][str(ref.chapter)][str(ref.verse)]
