import json
import os
from time import time

import ecce.influx
import ecce.model.nave.data as data
import ecce.nave as nave
import ecce.passage as passage
import pandas as pd
from ecce.constants import *
from ecce.model.ecce import EcceModel
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

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


category_frame = pd.read_csv(NAVE_CATEGORY_NODES, sep='\t')

processed_data = pd.read_csv(NLP_TOPICS_PATH, sep='\t')


@memoize
def model():
    return EcceModel(os.environ['ECCE_TOPIC_WEIGHTS'],
                     os.environ['ECCE_TSK_WEIGHTS'])


# ============
# Handlers
# ============


@app.post('/api/predict')
def predict(text: str, request: Request):
    start = time()
    result = model().predict(text)
    ecce.influx.record('ecce_predict', dict(
        text=text, duration=time() - start), request)

    topics = _as_dict(pd.DataFrame(result.topics))
    clusters = _as_dict(pd.DataFrame(result.clusters))
    return {'topics': topics, 'clusters': clusters}


@app.get('/api/esv/references')
def read_references():
    return references


@app.get('/api/esv/text/{book}/{chapter}/{verse}')
def text(book: str, chapter: int, verse: int, request: Request):
    ecce.influx.record('esv_text', dict(
        book=book, chapter=chapter, verse=verse), request)
    try:
        return {'text': esv[book][str(chapter)][str(verse)]}
    except KeyError as e:
        return {'error': str(e), 'type': 'KeyError'}


@app.get('/api/data/{book}/{chapter}/{verse}')
def data_line(book: str, chapter: int, verse: int, request: Request):
    ecce.influx.record('data', dict(book=book, chapter=chapter, verse=verse),
                       request)
    df = processed_data
    results = df[(df.book == book) & (df.chapter == chapter) &
                 (df.verse == verse)]
    if len(results) == 1:
        return _first_row_as_dict(results)
    else:
        return {'error': 'No reference found', 'type': 'KeyError'}


@app.get('/api/data/stats')
def stats(request: Request):
    start = time()
    stats = {
        'topics': _as_dict(data.topic_counts()),
        'verses': _as_dict(data.verse_counts())
    }
    ecce.influx.record('stats', dict(duration=time() - start), request)
    return stats


@app.get('/api/nave/topics')
def topic_nodes(request: Request,
                query: str = '',
                limit: int = 20,
                references: bool = False):
    ecce.influx.record('topics_index', dict(query=query), request)
    return _as_dict(
        nave.topics_matching_extracted(query,
                                       references=references).iloc[0:limit])


@app.get('/api/nave/topic/{topic_id}')
def topic_node(request: Request, topic_id: str, references: bool = True):
    ecce.influx.record('topics_show',
                       dict(topic_id=topic_id, include_references=references),
                       request)
    df = nave.by_topic_nodes(references=references)
    results = df[df.id == topic_id]

    if len(results) == 1:
        return _first_row_as_dict(results)
    else:
        return {'error': 'No topic found', 'type': 'KeyError'}


@app.get('/api/nave/topics/{topic_id}/categories')
def category_nodes(topic_id: str, request: Request):
    ecce.influx.record('categories_show', dict(topic_id=topic_id), request)
    return _as_dict(category_frame[category_frame.topic_id == topic_id])


@app.get('/api/nave/topics/{topic_id}/passages')
def topic_passages(topic_id: str, request: Request):
    ecce.influx.record('passages_index', dict(topic_id=topic_id), request)
    df = nave.by_topic_nodes(references=True)
    results = df[df.id == topic_id]

    if len(results) != 1:
        return {'error': 'No topic found', 'type': 'KeyError'}

    return pipe(results.iloc[0].at['references'], passage.init, passage.text,
                pd.DataFrame, _as_dict)


@app.get('/api/nave/reference/{book}/{chapter}/{verse}')
def topic_data_by_reference(book: str, chapter: int, verse: int,
                            request: Request):
    ecce.influx.record('topic_by_reference',
                       dict(book=book, chapter=chapter, verse=verse), request)
    try:
        return _as_dict(
            pd.DataFrame(nave_references[book][str(chapter)][str(verse)]))
    except KeyError as e:
        return {'error': str(e), 'type': 'KeyError'}


@app.get('/api/passages/default')
def default_passages():
    return pipe(
        "Joh3:16; Jer29:11; Ge1:1; Php4:13; Ro8:28; Ps23:1-6; Php4:6; Mt28:19; Eph2:8; Ga5:22; Ro12:1",
        nave.parse, passage.init, passage.text, pd.DataFrame, _as_dict)
