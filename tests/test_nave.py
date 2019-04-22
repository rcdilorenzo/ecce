import ecce.nave as nave
import ecce.reference as reference
import ecce.passage as passage

def describe_nave():

    def describe_topics_frame():

        def single():
            p = passage.init([reference.Data('Genesis', 1, 1)])[0]
            frame = nave.topics_frame(p)
            assert frame.label.iloc[0] == 'TIME'
            assert len(frame) == 7

        def multiple():
            p = passage.init([reference.Data('Genesis', 1, 1)])
            frame = nave.topics_frame(p)
            assert frame.label.iloc[0] == 'TIME'
            assert len(frame) == 7

    def describe_finding_topics_from_extracted():

        def describe_best_match_topic_for():

            def exact_match():
                # Should not return "WORD OF GOD" even though more topics
                # because match is exact
                result = nave.best_match_topic_for('WORD')
                assert result['label'] == 'WORD'

            def ambiguous_match():
                result = nave.best_match_topic_for('wor')
                assert result['label'] == 'WORD OF GOD'

            def removing_parentheses():
                result = nave.best_match_topic_for('WICKED PEOPLE')
                assert result['label'] == 'WICKED (PEOPLE)'

            def no_match():
                result = nave.best_match_topic_for('i love cheese')
                assert result == None


    def describe_reference_parsing():

        def single():
            assert nave.parse('Mt14:6') == [reference.Data('Matthew', 14, 6)]

        def single_with_book_number():
            assert nave.parse('1Ch4:2') == [reference.Data('1 Chronicles', 4, 2)]

        def non_canonical():
            assert nave.parse('Da14:1') == []

        def two_verses():
            assert nave.parse('Ex32:19,25') == [
                reference.Data('Exodus', 32, 19),
                reference.Data('Exodus', 32, 25)
            ]

        def multiple_verses():
            assert nave.parse('Jer35:6,8,16,19') == [
                reference.Data('Jeremiah', 35, 6),
                reference.Data('Jeremiah', 35, 8),
                reference.Data('Jeremiah', 35, 16),
                reference.Data('Jeremiah', 35, 19)
            ]

        def contiguous_verses():
            assert nave.parse('Jud21:19-21') == [
                reference.Data('Judges', 21, 19),
                reference.Data('Judges', 21, 20),
                reference.Data('Judges', 21, 21)
            ]

        def contiguous_and_non_contiguous_verses():
            assert nave.parse('Jud21:10,19-21') == [
                reference.Data('Judges', 21, 10),
                reference.Data('Judges', 21, 19),
                reference.Data('Judges', 21, 20),
                reference.Data('Judges', 21, 21)
            ]

        def multiple_chapters():
            assert nave.parse('De2:17,18:1-2; Ge2:1') == [
                reference.Data('Deuteronomy', 2, 17),
                reference.Data('Deuteronomy', 18, 1),
                reference.Data('Deuteronomy', 18, 2),
                reference.Data('Genesis', 2, 1)
            ]

        def multiple():
            assert nave.parse('Ex15:20; Ex32:19; Jud11:34') == [
                reference.Data('Exodus', 15, 20),
                reference.Data('Exodus', 32, 19),
                reference.Data('Judges', 11, 34)
            ]

        def similar_book_names():
            assert nave.parse('Jude1:3-4; Jud1:1') == [
                reference.Data('Jude', 1, 3),
                reference.Data('Jude', 1, 4),
                reference.Data('Judges', 1, 1)
            ]

