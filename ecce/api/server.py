import json

import pandas as pd
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from ecce.constants import *
import ecce.modeling.data as data

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'])

with open(ESV_PATH) as f:
    esv = json.load(f)

    references = {
        book: {
            chapter: sorted([int(k) for k in verses])[-1]
            for chapter, verses in chapters.items()
        }
        for book, chapters in esv.items()
    }

with open(NAVE_EXPORT_REF) as f:
    nave_references = json.load(f)


def _as_dict(df):
    return {
        'columns': df.columns.tolist(),
        'rows': json.loads(df.to_json(orient='values'))
    }


def _first_row_as_dict(df):
    return dict(zip(df.columns.tolist(), df.values.tolist()[0]))


topic_node_data = _as_dict(pd.read_csv(NAVE_TOPIC_NODES, sep='\t'))
category_frame = pd.read_csv(NAVE_CATEGORY_NODES, sep='\t')

processed_data = pd.read_csv(NLP_TOPICS_PATH, sep='\t')

# ============
# Handlers
# ============


@app.get('/api/esv/references')
def read_references():
    return references


@app.get('/api/esv/text/{book}/{chapter}/{verse}')
def text(book: str, chapter: int, verse: int):
    try:
        return {'text': esv[book][str(chapter)][str(verse)]}
    except KeyError as e:
        return {'error': str(e), 'type': 'KeyError'}


@app.get('/api/data/{book}/{chapter}/{verse}')
def data_line(book: str, chapter: int, verse: int):
    df = processed_data
    results = df[(df.book == book) & (df.chapter == chapter) &
                 (df.verse == verse)]
    if len(results) == 1:
        return _first_row_as_dict(results)
    else:
        return {'error': 'No reference found', 'type': 'KeyError'}


@app.get('/api/data/stats')
def stats():
    return {
        'topics': _as_dict(data.topic_counts()),
        'verses': _as_dict(data.verse_counts())
    }


@app.get('/api/nave/topics')
def topic_nodes():
    return topic_node_data


@app.get('/api/nave/reference/{book}/{chapter}/{verse}')
def topic_data_by_reference(book: str, chapter: int, verse: int):
    try:
        return _as_dict(
            pd.DataFrame(nave_references[book][str(chapter)][str(verse)]))
    except KeyError as e:
        return {'error': str(e), 'type': 'KeyError'}


@app.get('/api/nave/topics/{topic_id}/categories')
def category_nodes(topic_id: str):
    return _as_dict(category_frame[category_frame.topic_id == topic_id])
