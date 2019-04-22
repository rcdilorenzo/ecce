import math

import ecce.model.tsk.cluster_result as cluster_result
import ecce.tsk as tsk
import ecce.passage as passage
import ecce.reference as reference

def describe_cluster_result():

    def init():
        row = tsk.init().iloc[0]
        result = cluster_result.init(0.4, row.uuid)

        assert result.uuid == row.uuid
        assert result.probability == 0.4
        assert result.reference.book == row.linked_book
        assert result.reference.chapter == row.linked_chapter
        assert result.reference.verse == row.linked_verse
        assert result.text
        assert len(result.passages) > 0
        assert result.passages[0].text == None

    def describe_tf_idf():
        blank = None

        topic_1_id = 'topic_1_id'
        topic_2_id = 'topic_2_id'

        passage1 = passage.init([reference.init('Genesis', 1, 2)])[0]
        passage2 = passage.init([reference.init('Exodus', 5, 1)])[0]
        passage3 = passage.init([reference.init('John', 3, 16)])[0]

        sample = [
            cluster_result.ClusterResult(0.5, 'sd281x', blank, blank, [passage1]),
            cluster_result.ClusterResult(0.25, 'ds432a', blank, blank, [passage2, passage3])
        ]

        passage_to_topic_ids = {
            passage1.name: [topic_1_id],
            passage2.name: [topic_1_id, topic_2_id],
            passage3.name: [topic_2_id]
        }


        def to_tf_idf_topics():
            result = cluster_result.to_tf_idf_topics(sample, passage_to_topic_ids)

            assert result == [
                [(topic_1_id, 1 * math.log(3 / 2))],
                [(topic_1_id, 1 * math.log(3 / 2)), (topic_2_id, 2 * math.log(3 / 2))]
            ]

        def to_mean_weighted_tf_idf_topics():
            result = cluster_result.to_mean_weighted_tf_idf_topics(sample, passage_to_topic_ids)
            mean = lambda values: sum(values) / float(len(values))
            print(result)

            assert result == [
                (topic_2_id, 0.25 * 2 * math.log(3 / 2)),
                (topic_1_id, mean([0.5 * 1 * math.log(3 / 2), 0.25 * 1 * math.log(3 / 2)]))
            ]




