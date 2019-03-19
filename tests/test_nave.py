import ecce.nave as nave
import ecce.reference as reference

def describe_nave():

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

        def mutliple():
            assert nave.parse('Ex15:20; Ex32:19; Jud11:34') == [
                reference.Data('Exodus', 15, 20),
                reference.Data('Exodus', 32, 19),
                reference.Data('Judges', 11, 34)
            ]

