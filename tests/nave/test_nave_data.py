import ecce.modeling.nave.data as data

def describe_data():
    def describe_frame():
        def parsing_topics():
            row = data.frame().iloc[0]
            assert not isinstance(row.topics, str)
            assert len(row.topics) > 0

        def excluding_missing_topics():
            assert 0 not in data.frame().topics.apply(len).value_counts().index

    def topic_encoder():
        encoder = data.topic_encoder()
        assert encoder.classes_.shape[0] > 1000

    def text_tokenizer():
        tokenizer = data._text_tokenizer()
        assert len(tokenizer.word_counts) > 1000

    def tokenize():
        width = data._text_tokenizer().num_words
        encoded = data.tokenize(['God is good.', 'God is great.'])

        # Two sentences padded with zeros to max length
        assert encoded.shape == (2, width)
        assert encoded.sum() > 0
        assert encoded[:, 2:].sum() == 0

        # Encoded values match: 'God' == 'God'
        assert encoded[0][0] == encoded[1][0]
