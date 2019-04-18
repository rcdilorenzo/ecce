import logging
import os
import uuid

import keras.models
import numpy as np
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import *
from keras.layers.embeddings import Embedding
from keras.optimizers import *
from toolz import first, memoize, pipe

import ecce.modeling.tsk.data as data
from ecce.constants import CHECKPOINTS_PATH
from ecce.modeling.text import DEFAULT_SVD_COMPONENTS


class ClusterModel():
    def __init__(self):
        "Initialize model"

    def name(self):
        return 'tsk-cluster'

    def train(self, epochs=20, patience=3):
        self.epochs = epochs
        self.patience = patience

        logging.info('Splitting train/val/test data...')
        (vector_train, vector_test, cluster_train, cluster_test) = data.data_split()
        self.vector_train = vector_train
        self.vector_test = vector_test
        self.cluster_train = cluster_train
        self.cluster_test = cluster_test
        self.uuid = uuid.uuid4().hex[0:6]

        logging.info('Training...')
        self.model.summary()

        self.model.fit(
            self.vector_train,
            self.cluster_train,
            epochs=self.epochs,
            batch_size=256,
            validation_split=0.15,
            callbacks=self.callbacks())

    @property
    @memoize
    def model(self):
        uuid_count = len(data.uuid_encoder().categories_[0])

        inputs = Input(shape=(DEFAULT_SVD_COMPONENTS,))

        outputs = pipe(
            inputs,
            Dense(uuid_count, activation='softmax'))

        _model = keras.models.Model(inputs=inputs, outputs=outputs)

        optimizer = Adam()

        _model.compile(
            loss='categorical_crossentropy',
            optimizer=optimizer,
            metrics=['categorical_accuracy'])

        return _model

    def predict(self, text):
        result = self.model.predict(data.tokenize([text]))

        print(result)

        probabilities = list(result[result >= threshold])

        chosen = np.copy(result)
        chosen[(result[:] >= threshold)] = 1
        chosen[(result[:] < threshold)] = 0

        clusters = data.uuid_encoder().inverse_transform(chosen)[0]
        return list(reversed(sorted(zip(probabilities, clusters), key=first)))


    def callbacks(self):
        return [
            ModelCheckpoint(
                os.path.join(CHECKPOINTS_PATH, f'{self.name()}-{self.uuid}.hdf5'),
                save_best_only=True),
            EarlyStopping(patience=self.patience)
        ]

    def evaluate(self):
        print('Evaluating...')
        scores = self.model.evaluate(self.vector_test, self.cluster_test)
        print(f'Accuracy {scores[1] * 100:.2f}%')
