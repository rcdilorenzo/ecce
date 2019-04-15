import ecce.passage as passage
import ecce.reference as reference

def describe_passage():

    def contiguous_verses():
        assert passage.init([
            reference.init('Genesis', 1, 2),
            reference.init('Genesis', 1, 1)
        ]) == [
            passage.Data('Genesis 1:1-2', [
                reference.init('Genesis', 1, 1),
                reference.init('Genesis', 1, 2)
            ], None)
        ]

    def mixed_verses():
        assert passage.init([
            reference.init('Genesis', 1, 5),
            reference.init('Genesis', 1, 2),
            reference.init('Genesis', 1, 1)
        ]) == [
            passage.Data('Genesis 1:1-2,5', [
                reference.init('Genesis', 1, 1),
                reference.init('Genesis', 1, 2),
                reference.init('Genesis', 1, 5)
            ], None)
        ]

    def multiple_chapters():
        assert passage.init([
            reference.init('Genesis', 1, 5),
            reference.init('Genesis', 1, 2),
            reference.init('Genesis', 3, 12),
            reference.init('Genesis', 3, 10),
            reference.init('Genesis', 1, 1)
        ]) == [
            passage.Data('Genesis 1:1-2,5', [
                reference.init('Genesis', 1, 1),
                reference.init('Genesis', 1, 2),
                reference.init('Genesis', 1, 5)
            ], None),
            passage.Data('Genesis 3:10,12', [
                reference.init('Genesis', 3, 10),
                reference.init('Genesis', 3, 12)
            ], None),
        ]

    def multiple_books():
        assert passage.init([
            reference.init('Genesis', 1, 5),
            reference.init('Genesis', 1, 2),
            reference.init('Exodus', 5, 3),
            reference.init('Genesis', 3, 12),
            reference.init('Revelation', 1, 1),
            reference.init('Genesis', 3, 10),
            reference.init('Genesis', 1, 1)
        ]) == [
            passage.Data('Genesis 1:1-2,5', [
                reference.init('Genesis', 1, 1),
                reference.init('Genesis', 1, 2),
                reference.init('Genesis', 1, 5)
            ], None),
            passage.Data('Genesis 3:10,12', [
                reference.init('Genesis', 3, 10),
                reference.init('Genesis', 3, 12)
            ], None),
            passage.Data('Exodus 5:3', [
                reference.init('Exodus', 5, 3)
            ], None),
            passage.Data('Revelation 1:1', [
                reference.init('Revelation', 1, 1)
            ], None)
        ]

    def duplicates():
        assert passage.init([
            reference.init('Genesis', 1, 2),
            reference.init('Genesis', 1, 2),
            reference.init('Genesis', 1, 1)
        ]) == [
            passage.Data('Genesis 1:1-2', [
                reference.init('Genesis', 1, 1),
                reference.init('Genesis', 1, 2)
            ], None)
        ]

    def describe_text():
        def single_verse():
            assert passage.text([
                passage.Data('Genesis 1:2', [
                    reference.init('Genesis', 1, 2)
                ], None)
            ]) == [
                passage.Data(
                    'Genesis 1:2',
                    [ reference.init('Genesis', 1, 2) ],
                    'The earth was without form and void, and darkness was over the face of the deep. And the Spirit of God was hovering over the face of the waters.'
                )
            ]

        def multiple_verses():
            assert passage.text([
                passage.Data('Genesis 1:2-3', [
                    reference.init('Genesis', 1, 2),
                    reference.init('Genesis', 1, 3)
                ], None)
            ]) == [
                passage.Data('Genesis 1:2-3', [
                    reference.init('Genesis', 1, 2),
                    reference.init('Genesis', 1, 3)
                ], '2 The earth was without form and void, and darkness was over the face of the deep. And the Spirit of God was hovering over the face of the waters.\n3 And God said, "Let there be light," and there was light.')
            ]
