import numpy as np

import ecce.tsk as tsk
from ecce.reference import Reference

def describe_tsk():

    def describe_reference_parsing():

        def multiple():
            assert tsk.parse('pr 8:22-24;pr 16:4;mr 13:19;joh 1:1-3;heb 1:10;1jo 1:1') == [
                Reference('Proverbs', 8, 22),
                Reference('Proverbs', 8, 23),
                Reference('Proverbs', 8, 24),
                Reference('Proverbs', 16, 4),
                Reference('Mark', 13, 19),
                Reference('John', 1, 1),
                Reference('John', 1, 2),
                Reference('John', 1, 3),
                Reference('Hebrews', 1, 10),
                Reference('1 John', 1, 1)
            ]


    def find_by_uuid():
        uuid = tsk.init().uuid[0]

        assert len(tsk.find_by_uuid(uuid)) > 1

    def passages_by_uuid():
        uuid = tsk.init().uuid[0]

        passages = tsk.passages_by_uuid(uuid, include_text=True)
        assert len(passages) > 1

        passage = passages[0]
        assert passage.name is not None
        assert len(passage.references) > 0
        assert passage.text is not None


