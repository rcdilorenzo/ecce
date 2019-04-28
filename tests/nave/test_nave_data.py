import ecce.model.nave.data as data

def describe_data():
    def describe_frame():
        def parsing_topics():
            row = data.frame().iloc[0]
            assert not isinstance(row.topics, str)
            assert len(row.topics) > 0

        def excluding_missing_topics():
            assert 0 not in data.frame().topics.apply(len).value_counts().index

    def topic_chunk_encoder():
        encoder = data.topic_chunk_encoder()
        assert encoder.classes_.shape[0] > 1000
