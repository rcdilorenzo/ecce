import logging
import os
import uuid

import ecce.model.nave.data as data
import ecce.model.nave.topic_result as topic_result
import numpy as np
from ecce.constants import CHECKPOINTS_PATH
from keras.callbacks import EarlyStopping, ModelCheckpoint
from collections import namedtuple as Struct
from toolz import first, pipe
from funcy import distinct, rpartial
from ecce.utils import *

class Model():
    def load_weights(self, name):
        self.model.load_weights(name)

    def train(self, epochs=20, patience=3):
        self.epochs = epochs
        self.patience = patience

        logging.info('Splitting train/val/test data...')
        (text_train, text_test, topics_train, topics_test) = data.data_split()
        self.text_train = text_train
        self.text_test = text_test
        self.topics_train = topics_train
        self.topics_test = topics_test
        self.uuid = uuid.uuid4().hex[0:6]

        logging.info('Training...')
        self.model.summary()

        self.model.fit(
            self.text_train,
            self.topics_train,
            epochs=self.epochs,
            batch_size=256,
            validation_split=0.15,
            callbacks=self.callbacks())

    def predict(self, text, threshold=0.5):
        tokens = data.tokenize([text])
        result = self.model.predict(tokens)

        probabilities = list(result[result >= threshold])

        chosen = np.copy(result)
        chosen[(result[:] >= threshold)] = 1
        chosen[(result[:] < threshold)] = 0

        topic_chunks = data.topic_chunk_encoder().inverse_transform(chosen)[0]

        return pipe(
            zip(probabilities, topic_chunks),
            sorted(key=first),
            reversed,
            list_map(lambda x: topic_result.init(*x)),
            rpartial(distinct, attr('id')))


    def callbacks(self):
        return [
            ModelCheckpoint(
                os.path.join(CHECKPOINTS_PATH, f'{self.name()}-{self.uuid}.hdf5'),
                save_best_only=True),
            EarlyStopping(patience=self.patience)
        ]

    def evaluate(self):
        print('Evaluating...')
        scores = self.model.evaluate(self.text_test, self.topics_test)
        print(f'Accuracy {scores[1] * 100:.2f}%')

    @property
    def model(self):
        return None
