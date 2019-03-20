import ecce.reference as reference
import ecce.passage as passage

def describe_passage():

    def contiguous_verses():
        assert passage.init([
            reference.init('Genesis', 1, 2),
            reference.init('Genesis', 1, 1)
        ]) == [passage.Data(
            'Genesis 1:1-2',
            [
                reference.init('Genesis', 1, 1),
                reference.init('Genesis', 1, 2)
            ]
        )]

    def mixed_verses():
        assert passage.init([
            reference.init('Genesis', 1, 5),
            reference.init('Genesis', 1, 2),
            reference.init('Genesis', 1, 1)
        ]) == [passage.Data(
            'Genesis 1:1-2,5',
            [
                reference.init('Genesis', 1, 1),
                reference.init('Genesis', 1, 2),
                reference.init('Genesis', 1, 5)
            ]
        )]

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
            ]),
            passage.Data('Genesis 3:10,12', [
                reference.init('Genesis', 3, 10),
                reference.init('Genesis', 3, 12)
            ]),
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
            ]),
            passage.Data('Genesis 3:10,12', [
                reference.init('Genesis', 3, 10),
                reference.init('Genesis', 3, 12)
            ]),
            passage.Data('Exodus 5:3', [
                reference.init('Exodus', 5, 3)
            ]),
            passage.Data('Revelation 1:1', [
                reference.init('Revelation', 1, 1)
            ])
        ]
