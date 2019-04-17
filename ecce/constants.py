import logging

from ecce.utils import *

logging.basicConfig(level=logging.DEBUG)

DATA_PATH = relative_path(__file__, 'data')
EXPORT_PATH = relative_path(__file__, 'data/exported')
CACHE_PATH = relative_path(__file__, 'data/cache')
CHECKPOINTS_PATH  = relative_path(__file__, 'data/checkpoints/')


if os.path.isdir(DATA_PATH) is False: os.mkdir(DATA_PATH)
if os.path.isdir(EXPORT_PATH) is False: os.mkdir(EXPORT_PATH)
if os.path.isdir(CACHE_PATH) is False: os.mkdir(CACHE_PATH)
if os.path.isdir(CHECKPOINTS_PATH) is False: os.mkdir(CHECKPOINTS_PATH)

MIN_VERSES_PER_TOPIC = 30

ESV_PATH            = relative_path(__file__, 'data/ESV.json')
NAVE_CAT_PATH       = relative_path(__file__, 'data/nave/categories.txt')
NAVE_TOPIC_PATH     = relative_path(__file__, 'data/nave/topics.txt')
NAVE_SUBTOPIC_PATH  = relative_path(__file__, 'data/nave/subtopics.txt')
NAVE_REF_PATH       = relative_path(__file__, 'data/nave/topicxref.txt')
NAVE_FRAME_PATH     = relative_path(__file__, 'data/nave/parsed.csv')
NAVE_PATH           = relative_path(__file__, 'data/nave/pickled.obj')
TSK_PATH            = relative_path(__file__, 'data/tsk/parsed.csv')
TSK_RAW_PATH        = relative_path(__file__, 'data/tsk/tskxref.txt')

GLOVE_PATH          = relative_path(__file__, 'data/glove/glove.42B.300d.txt')
GLOVE_WORD2VEC_PATH = GLOVE_PATH + '.word2vec'
WORD_EMBEDDINGS     = relative_path(__file__, 'data/word-embeddings.npy')

NAVE_EXPORT_TOPIC    = os.path.join(EXPORT_PATH, 'nave-by-topic.json')
NAVE_EXPORT_REF      = os.path.join(EXPORT_PATH, 'nave-by-reference.json')
NAVE_SUBTOPIC_NODES  = os.path.join(EXPORT_PATH, 'nave-subtopic-nodes.tsv')
NAVE_CATEGORY_NODES  = os.path.join(EXPORT_PATH, 'nave-category-nodes.tsv')
NAVE_TOPIC_NODES     = os.path.join(EXPORT_PATH, 'nave-topic-nodes.tsv')
NAVE_EXPORT_PASSAGES = os.path.join(EXPORT_PATH, 'nave-passages.json')

CACHE_VERSE_COUNTS = os.path.join(CACHE_PATH, 'verse-counts-{}.csv')
CACHE_TSK_CLUSTERS = os.path.join(CACHE_PATH, 'tsk-clusters.obj')

NLP_TOPICS_PATH     = os.path.join(EXPORT_PATH, 'verse-with-topics.tsv')

NAVE_ABBREVIATIONS = {
    'Ge': 'Genesis',
    'Ex': 'Exodus',
    'Le': 'Leviticus',
    'Nu': 'Numbers',
    'De': 'Deuteronomy',
    'Jos': 'Joshua',
    'Jud': 'Judges',
    'Ru': 'Ruth',
    '1Sa': '1 Samuel',
    '2Sa': '2 Samuel',
    '1Ki': '1 Kings',
    '2Ki': '2 Kings',
    '1Ch': '1 Chronicles',
    '2Ch': '2 Chronicles',
    'Ezr': 'Ezra',
    'Ne': 'Nehemiah',
    'Es': 'Esther',
    'Job': 'Job',
    'Ps': 'Psalms',
    'Pr': 'Proverbs',
    'Ec': 'Ecclesiastes',
    'So': 'Song of Solomon',
    'Isa': 'Isaiah',
    'Jer': 'Jeremiah',
    'La': 'Lamentations',
    'Eze': 'Ezekiel',
    'Da': 'Daniel',
    'Ho': 'Hosea',
    'Joe': 'Joel',
    'Am': 'Amos',
    'Ob': 'Obadiah',
    'Jon': 'Jonah',
    'Mic': 'Micah',
    'Na': 'Nahum',
    'Hab': 'Habakkuk',
    'Zep': 'Zephaniah',
    'Hag': 'Haggai',
    'Zec': 'Zechariah',
    'Mal': 'Malachi',
    'Mt': 'Matthew',
    'Mr': 'Mark',
    'Lu': 'Luke',
    'Joh': 'John',
    'Ac': 'Acts',
    'Ro': 'Romans',
    '1Co': '1 Corinthians',
    '2Co': '2 Corinthians',
    'Ga': 'Galatians',
    'Eph': 'Ephesians',
    'Php': 'Philippians',
    'Col': 'Colossians',
    '1Th': '1 Thessalonians',
    '2Th': '2 Thessalonians',
    '1Ti': '1 Timothy',
    '2Ti': '2 Timothy',
    'Tit': 'Titus',
    'Phm': 'Philemon',
    'Heb': 'Hebrews',
    'Jas': 'James',
    '1Pe': '1 Peter',
    '2Pe': '2 Peter',
    '1Jo': '1 John',
    '2Jo': '2 John',
    '3Jo': '3 John',
    'Jude': 'Jude',
    'Re': 'Revelation'
}

TSK_ABBREVIATIONS = {
    'ge': 'Genesis',
    'ex': 'Exodus',
    'le': 'Leviticus',
    'nu': 'Numbers',
    'de': 'Deuteronomy',
    'jos': 'Joshua',
    'jud': 'Judges',
    'ru': 'Ruth',
    '1sa': '1 Samuel',
    '2sa': '2 Samuel',
    '1ki': '1 Kings',
    '2ki': '2 Kings',
    '1ch': '1 Chronicles',
    '2ch': '2 Chronicles',
    'ezr': 'Ezra',
    'ne': 'Nehemiah',
    'es': 'Esther',
    'job': 'Job',
    'ps': 'Psalms',
    'pr': 'Proverbs',
    'ec': 'Ecclesiastes',
    'so': 'Song of Solomon',
    'isa': 'Isaiah',
    'jer': 'Jeremiah',
    'la': 'Lamentations',
    'eze': 'Ezekiel',
    'da': 'Daniel',
    'ho': 'Hosea',
    'joe': 'Joel',
    'am': 'Amos',
    'ob': 'Obadiah',
    'jon': 'Jonah',
    'mic': 'Micah',
    'na': 'Nahum',
    'hab': 'Habakkuk',
    'zep': 'Zephaniah',
    'hag': 'Haggai',
    'zec': 'Zechariah',
    'mal': 'Malachi',
    'mt': 'Matthew',
    'mr': 'Mark',
    'lu': 'Luke',
    'joh': 'John',
    'ac': 'Acts',
    'ro': 'Romans',
    '1co': '1 Corinthians',
    '2co': '2 Corinthians',
    'ga': 'Galatians',
    'eph': 'Ephesians',
    'php': 'Philippians',
    'col': 'Colossians',
    '1th': '1 Thessalonians',
    '2th': '2 Thessalonians',
    '1ti': '1 Timothy',
    '2ti': '2 Timothy',
    'tit': 'Titus',
    'phm': 'Philemon',
    'heb': 'Hebrews',
    'jas': 'James',
    '1pe': '1 Peter',
    '2pe': '2 Peter',
    '1jo': '1 John',
    '2jo': '2 John',
    '3jo': '3 John',
    'jude': 'Jude',
    're': 'Revelation'
}

CANONICAL_ORDER = [
    'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
    'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings',
    '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job',
    'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah',
    'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos',
    'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai',
    'Zechariah', 'Malachi', 'Matthew', 'Mark', 'Luke', 'John', 'Acts',
    'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
    'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
    '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James',
    '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation'
]
