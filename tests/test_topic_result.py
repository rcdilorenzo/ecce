import ecce.model.nave.topic_result as topic_result

def describe_topic_result():

    def describe_init():

        def exact_match():
            result = topic_result.init(0.5, 'WORD')
            assert result.id == 'tpc:-197895800'
            assert result.probability == 0.5
            assert result.label == 'WORD'

        def ambiguous_match():
            result = topic_result.init(0.4, 'JESUS')

            assert result.id == 'tpc:-314322582'
            assert result.probability == 0.4
            assert result.label == 'JESUS, THE CHRIST'
