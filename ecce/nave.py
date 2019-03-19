from ecce.utils import *
import ecce.reference as ref
from pymonad.Maybe import *
from funcy import first, flatten
from toolz.curried import *
from lenses import lens


NAVE_ABBREVIATIONS = {
    'Ge': 'Genesis', 'Ex': 'Exodus', 'Le': 'Leviticus', 'Nu': 'Numbers',
    'De': 'Deuteronomy', 'Jos': 'Joshua', 'Jud': 'Judges', 'Ru': 'Ruth',
    '1Sa': '1 Samuel', '2Sa': '2 Samuel', '1Ki': '1 Kings', '2Ki': '2 Kings',
    '1Ch': '1 Chronicles', '2Ch': '2 Chronicles', 'Ezr': 'Ezra',
    'Ne': 'Nehemiah', 'Es': 'Esther', 'Job': 'Job', 'Ps': 'Psalms',
    'Pr': 'Proverbs', 'Ec': 'Ecclesiates', 'So': 'Song of Solomon',
    'Isa': 'Isaiah', 'Jer': 'Jeremiah', 'La': 'Lamentations', 'Eze': 'Ezekiel',
    'Da': 'Daniel', 'Ho': 'Hosea', 'Joe': 'Joel', 'Am': 'Amos',
    'Ob': 'Obadiah', 'Jon': 'Jonah', 'Mic': 'Micah', 'Na': 'Nahum',
    'Hab': 'Habakkuk', 'Zep': 'Zephaniah', 'Hag': 'Haggi', 'Zec': 'Zechariah',
    'Mal': 'Malachi', 'Mt': 'Matthew', 'Mr': 'Mark', 'Lu': 'Luke',
    'Joh': 'John', 'Ac': 'Acts', 'Ro': 'Romans', '1Co': '1 Corinthians',
    '2Co': '2 Corinthians', 'Ga': 'Galatians', 'Eph': 'Ephesians',
    'Php': 'Philippians', 'Col': 'Colossians', '1Th': '1 Thessalonians',
    '2Th': '2 Thessalonians', '1Ti': '1 Timothy', '2Ti': '2 Timothy',
    'Tit': 'Titus', 'Phm': 'Philemon', 'Heb': 'Hebrews', 'Jas': 'James',
    '1Pe': '1 Peter', '2Pe': '2 Peter', '1Jo': '1 John', '2Jo': '2 John',
    '3Jo': '3 John', 'Jude': 'Jude', 'Re': 'Revelation'
}

def parse(raw_reference):
    def _expand_book(raw):
        """Converts "Lu2:3,4,5" to ("Luke", "2:3,4,5")"""
        return pipe(
            NAVE_ABBREVIATIONS.keys(),
            list_filter(lambda k: k in raw),
            first,
            to_maybe,
        ) >> (
            lambda k: Just((NAVE_ABBREVIATIONS[k], raw.replace(k, '')))
        )

    def _expand_chapter(raw):
        """Converts "2:3,4,5" to (2, "3, 4, 5")"""
        chapter, verses = raw.split(':')
        return (int(chapter), verses)

    def _expand_verses(raw):
        """Converts "3,4,5" or "3-5" to [3, 4, 5]"""
        if '-' in raw:
            start, end = list_map(int, raw.split('-'))
            return list(range(start, end + 1))
        else:
            return list_map(int, raw.split(','))

    def _to_references(data):
        """Converts ('Luke', (2, [3, 4, 5])) to (List ref.Data)"""
        book, (chapter, verses) = data
        return map(
            lambda verse: to_maybe(ref.init(book, chapter, verse)),
            verses
        )

    return pipe(
        raw_reference.split('; '),

        # Initial text conversion
        map(mconcat_bind([
            to_maybe,
            _expand_book,
            compose(to_maybe, lens[1].modify(_expand_chapter)),
            compose(to_maybe, lens[1][1].modify(_expand_verses))
        ])),
        mcompact,

        # Convert data structure to validated ESV references
        map(_to_references),
        flatten,
        mcompact
    )

