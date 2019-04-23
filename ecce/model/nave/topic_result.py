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

    return TopicResult(probability, topic['id'], topic['label'])


def intersect_with_weighted_tf_idf(topic_results, weighted_tf_idf_topics):
    # TODO: Assess whether we should primarily use first or second argument
    #
    #     tf_idf_topic_ids = list_map(attr('topic_id'), weighted_tf_idf_topics)
    #     df = nave.by_topic_nodes()
    #     filtered = df[df.id.isin(tf_idf_topic_ids)]
    #     id_to_label = dict(zip(filtered.id, filtered.label))

    min_weight = min(*[topic.score for topic in weighted_tf_idf_topics])

    id_to_tf_idf = dict(weighted_tf_idf_topics)

    return list_map(
        lambda r: TopicResult(
            float(r.probability * id_to_tf_idf.get(r.id, min_weight)), r.id, r.label),
        topic_results)
