from ecce.constants import *
import json
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

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


topic_node_data = _as_dict(pd.read_csv(NAVE_TOPIC_NODES, sep='\t'))
category_frame = pd.read_csv(NAVE_CATEGORY_NODES, sep='\t')


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


@app.get('/api/nave/topics')
def topic_nodes():
    return topic_node_data


@app.get('/api/nave/reference/{book}/{chapter}/{verse}')
def topic_data_by_reference(book: str, chapter: int, verse: int):
    try:
        return _as_dict(pd.DataFrame(nave_references[book][str(chapter)][str(verse)]))
    except KeyError as e:
        return {'error': str(e), 'type': 'KeyError'}


@app.get('/api/nave/topics/{topic_id}/categories')
def category_nodes(topic_id: str):
    return _as_dict(category_frame[category_frame.topic_id == topic_id])
