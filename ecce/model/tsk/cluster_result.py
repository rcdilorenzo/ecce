import logging
import math
from collections import namedtuple as Struct
from funcy import cat, first, second, partial
from toolz.curried import pipe, map, groupby

from ecce.model.nave.topic_result import TopicResult
import ecce.tsk as tsk
import ecce.reference as reference
import ecce.nave as nave
import ecce.esv as esv
from ecce.utils import *

ClusterResult = Struct('ClusterResult', ['probability', 'uuid', 'reference', 'text', 'passages'])

# Note: Implementation requires two keys to transform to dictionary
WeightedTfIdfTopic = Struct('WeightedTfIdfTopic', ['topic_id', 'score'])


def init(probability, uuid):
    ref = reference.init_raw_row(
        tsk.find_by_uuid(uuid).iloc[0], prefix='linked_')

    return ClusterResult(float(probability), uuid, ref, esv.text(ref),
                         tsk.passages_by_uuid(uuid))


def to_mean_weighted_tf_idf_topics(cluster_results, passage_to_topic_ids=None):
    """Converts cluster results into topics of term frequency-inverse document
    frequency within the results and then weights them by the cluster's given
    probability

        term = topic
        document = list of topics for a given passage

    Example:

        [('tpc:-12894305', 0.134725), ...]

    """
    def _weight_tf_idf_pairs(pair):
        cluster_result, tf_idf_pairs = pair
        return [(topic_id, cluster_result.probability * tf_idf) for topic_id, tf_idf in tf_idf_pairs]

    def _average_tf_idf_pairs(pair):
        topic_id, tf_idf_pairs = pair
        return [(topic_id, mean(list_map(second, tf_idf_pairs)))]

    return pipe(
        to_tf_idf_topics(cluster_results, passage_to_topic_ids),
        partial(zip, cluster_results),
        map(_weight_tf_idf_pairs),
        cat,
        groupby(first),
        lambda d: d.items(),
        map(_average_tf_idf_pairs),
        cat,
        list_map(lambda t: WeightedTfIdfTopic(*t)),
        sorted(key=attr('score'), reverse=True))


def to_tf_idf_topics(cluster_results, passage_to_topic_ids=None):
    """Converts cluster results into topics of term frequency-inverse document
    frequency within the results

    TODO: and then weights them by the cluster's given probability

        term = topic
        document = list of topics for a given passage

    Example:

        [[('tpc:-12894305', 2.8903717), ...], ...]
    """

    return [
        tf_idf_topics_for(r, cluster_results, passage_to_topic_ids)
        for r in cluster_results
    ]


def tf_idf_topics_for(cluster_result,
                      cluster_results,
                      passage_to_topic_ids=None):
    """Converts cluster result into topics of term frequency-inverse document
    frequency

    Example:

        [('tpc:-12894305', 2.8903717), ...]
    """
    if passage_to_topic_ids is None:
        passage_to_topic_ids = topic_ids_by_passage_name(cluster_results)

    topic_id_counts = count_nested_reps(passage_to_topic_ids.values())

    passage_count = pipe(cluster_results, map(attr('passages')), cat, list,
                         len)

    def idf(topic_id, topic_id_counts):
        "Find inverse document frequency of topics amongst clusters"
        return math.log(passage_count / topic_id_counts[topic_id])

    "Convert cluster topic counts to tf_idf scores for topic occurrences"
    return [(topic_id, tf * idf(topic_id, topic_id_counts)) for topic_id, tf in
            topic_frequencies(cluster_result, passage_to_topic_ids)]


def topic_frequencies(cluster_result, passage_to_topic_ids):
    """Count topic frequencies in a given cluster result.

    Example:

        [('tpc:-19024835', 2), ...]
    """
    return list(
        count_nested_reps([
            count_reps(passage_to_topic_ids[p.name])
            for p in cluster_result.passages
        ]).items())


def topic_ids_by_passage_name(cluster_results):
    """Converts cluster results to dictionary of topic_id frequencies

    Example:

        {'Genesis 1:1-2': ['tpc:-294912854', ... ], ...}
    """
    passages = pipe(cluster_results, map(attr('passages')), cat, list)
    df = nave.topics_frame(passages)
    return {p.name: nave.topics_frame(p, df=df).id.tolist() for p in passages}
