import logging
from collections import namedtuple as Struct

import ecce.nave as nave

TopicResult = Struct('TopicResult', ['probability', 'id', 'label'])

def init(probability, topic_chunk):
    topic = nave.best_match_topic_for(topic_chunk)

    if topic is None:
        logging.warning(f'No topic found for match {topic_chunk}')

    return TopicResult(probability, topic['id'], topic['label'])




