from ecce.model.nave.model import NaveModel
from ecce.model.tsk.model import ClusterModel
import ecce.model.tsk.cluster_result as cr
import ecce.model.nave.topic_result as tr

from toolz import memoize
from collections import namedtuple as Struct

EcceModelResult = Struct('EcceResult', ['topics', 'clusters'])


class EcceModel():
    def __init__(self, topic_weights, cluster_weights):
        self.topic_weights = topic_weights
        self.cluster_weights = cluster_weights

    @property
    @memoize
    def topic_model(self):
        model = NaveModel()
        model.load_weights(self.topic_weights)
        return model

    @property
    @memoize
    def cluster_model(self):
        model = ClusterModel()
        model.load_weights(self.cluster_weights)
        return model

    def predict(self,
                text,
                topic_threshold=0.02,
                top_clusters=5,
                cluster_topic_pool_size=20,
                max_topics=10):

        topic_results = self.topic_model.predict(
            text, threshold=topic_threshold)
        cluster_results = self.cluster_model.predict(
            text, n_max=cluster_topic_pool_size)

        cluster_adjusted_topic_results = tr.intersect_with_weighted_tf_idf(
            topic_results,
            cr.to_mean_weighted_tf_idf_topics(cluster_results))[0:max_topics]

        return EcceModelResult(cluster_adjusted_topic_results,
                               cluster_results[0:top_clusters])
