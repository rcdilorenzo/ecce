import logging
import os
import uuid
from collections import namedtuple as Struct

import ecce.model.nave.data as data
import ecce.model.nave.topic_result as topic_result
import keras.models
import numpy as np
from ecce.constants import CHECKPOINTS_PATH
import ecce.model.text as text
from ecce.utils import *
from funcy import distinct, rpartial
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import *
from keras.layers.embeddings import Embedding
from keras.optimizers import *
from toolz import first, memoize, pipe


class NaveModel():
    def __init__(self):
        self._train_data_loaded = False

    @property
    @memoize
    def model(self):
        topic_count = len(data.topic_chunk_encoder().classes_)

        input_size = data.tokenize(['']).shape[1]

        inputs = Input(shape=(input_size,))

        outputs = pipe(
            inputs,
            Dense(topic_count * 3, activation='relu'),
            Dropout(0.3),
            Dense(topic_count, activation='sigmoid'))

        _model = keras.models.Model(inputs=inputs, outputs=outputs)

        optimizer = Adam(beta_1=0.75)

        _model.compile(
            loss='categorical_crossentropy',
            optimizer=optimizer,
            metrics=['categorical_accuracy'])

        return _model

    def load_weights(self, name):
        self.model.load_weights(name)

    def _load_train_data(self):
        if self._train_data_loaded is False:
            logging.info('Splitting train/val/test data...')
            (text_train, text_test, topics_train, topics_test) = data.data_split()
            self.text_train = text_train
            self.text_test = text_test
            self.topics_train = topics_train
            self.topics_test = topics_test
            self._train_data_loaded = True

    def train(self, epochs=20, patience=3):
        self.epochs = epochs
        self.patience = patience

        self._load_train_data()
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
            rpartial(distinct, attr('id')),
            list)


    def callbacks(self):
        return [
            ModelCheckpoint(
                os.path.join(CHECKPOINTS_PATH, f'nave-{self.uuid}.hdf5'),
                save_best_only=True),
            EarlyStopping(patience=self.patience)
        ]

    def evaluate(self):
        print('Evaluating...')
        self._load_train_data()
        scores = self.model.evaluate(self.text_test, self.topics_test)
        print(f'Accuracy {scores[1] * 100:.2f}%')
