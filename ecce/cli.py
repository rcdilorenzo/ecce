import simplejson
import os
import pandas as pd

import ecce.nave as nave
from ecce.constants import *
from ecce.modeling.tsk.model import ClusterModel
from ecce.modeling.nave.lstm_model import LstmModel
from ecce.modeling.nave.gru_model import GruModel

def train_tsk_clusters(args):
    model = ClusterModel()
    model.train(args.epochs, args.patience)
    model.evaluate()

def train_lstm(args):
    model = LstmModel()
    model.train(args.epochs, args.patience)
    model.evaluate()


def train_gru(args):
    model = GruModel()
    model.train(args.epochs, args.patience)
    model.evaluate()


def predict_lstm(args):
    model = LstmModel()
    model.load_weights(args.weights)

    print('\nEnter text to predict. Type "exit" when finished.')
    command = input('> ')
    while command != 'exit':
        results = model.predict(command, threshold=args.threshold)
        print('Result: ', results)
        command = input('\n> ')

    print('Exiting.')


def export_nave(args):
    print(f'Writing to {NAVE_EXPORT_REF}')
    if os.path.isfile(NAVE_EXPORT_REF) is False:
        with open(NAVE_EXPORT_REF, 'w') as f:
            simplejson.dump(nave.by_reference(), f, ignore_nan=True)

    print(f'Writing to {NAVE_EXPORT_TOPIC}')
    if os.path.isfile(NAVE_EXPORT_TOPIC) is False:
        with open(NAVE_EXPORT_TOPIC, 'w') as f:
            simplejson.dump(nave.by_topic(), f, ignore_nan=True)

    print(f'Writing to {NAVE_SUBTOPIC_NODES}')
    subtopic_nodes = nave.by_subtopic_nodes()
    if os.path.isfile(NAVE_SUBTOPIC_NODES) is False:
        columns = list(
            remove(lambda k: k == 'passages', subtopic_nodes.columns))
        (subtopic_nodes[columns].to_csv(
            NAVE_SUBTOPIC_NODES, sep='\t', index=False))

    print(f'Writing to {NAVE_EXPORT_PASSAGES}')
    subtopic_to_passages = dict(
        subtopic_nodes.apply(lambda r: (r.at['id'], r.at['passages']),
                             axis=1).tolist())
    if os.path.isfile(NAVE_EXPORT_PASSAGES) is False:
        with open(NAVE_EXPORT_PASSAGES, 'w') as f:
            simplejson.dump(subtopic_to_passages, f, ignore_nan=True)

    print(f'Writing to {NAVE_CATEGORY_NODES}')
    if os.path.isfile(NAVE_CATEGORY_NODES) is False:
        (nave.by_category_nodes().to_csv(
            NAVE_CATEGORY_NODES, sep='\t', index=False))

    print(f'Writing to {NAVE_TOPIC_NODES}')
    if os.path.isfile(NAVE_TOPIC_NODES) is False:
        (nave.by_topic_nodes().to_csv(NAVE_TOPIC_NODES, sep='\t', index=False))


def export_topics(args):
    print(f'Writing to {NLP_TOPICS_PATH}')
    if os.path.isfile(NLP_TOPICS_PATH) is False:
        (nave.topic_data_frame().to_csv(
            NLP_TOPICS_PATH, sep='\t', index=False))
