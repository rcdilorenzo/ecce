import logging
from ecce.utils import *

logging.basicConfig(level=logging.DEBUG)

ESV_PATH            = relative_path(__file__, '../data/ESV.json')
NAVE_CAT_PATH       = relative_path(__file__, '../data/nave/categories.txt')
NAVE_TOPIC_PATH    = relative_path(__file__, '../data/nave/topics.txt')
NAVE_SUBTOPIC_PATH = relative_path(__file__, '../data/nave/subtopics.txt')
NAVE_REF_PATH       = relative_path(__file__, '../data/nave/topicxref.txt')
NAVE_FRAME_PATH       = relative_path(__file__, '../data/nave/parsed.csv')
NAVE_PATH       = relative_path(__file__, '../data/nave/pickled.obj')

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
