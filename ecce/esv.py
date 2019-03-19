from ecce.constants import ESV_PATH

import json
import logging
from toolz import memoize

@memoize
def verses():
    with open(ESV_PATH) as f:
        logging.info('Loading ESV JSON...')
        return json.load(f)

def text(ref):
    return verses()[ref.book][str(ref.chapter)][str(ref.verse)]
