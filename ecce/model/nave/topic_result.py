import logging
from collections import namedtuple as Struct
import pandas as pd

import ecce.nave as nave
from ecce.utils import *

TopicResult = Struct('TopicResult', ['probability', 'id', 'label'])


def init(probability, topic_chunk):
    topic = nave.best_match_topic_for(topic_chunk)

    if topic is None:
        logging.warning(f'No topic found for match {topic_chunk}')

    return TopicResult(float(probability), topic['id'], topic['label'])

