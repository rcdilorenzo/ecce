import logging
import os
import uuid

import keras.models
import numpy as np
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import *
from keras.optimizers import *
from lenses import lens
from toolz import first, memoize, pipe, compose
from collections import namedtuple as Struct

import ecce.model.tsk.data as data
import ecce.tsk as tsk
from ecce.constants import CHECKPOINTS_PATH
from ecce.model.text import DEFAULT_SVD_COMPONENTS
import ecce.utils as utils
from ecce.utils import list_map

ClusterResult = Struct('ClusterResult', ['probability', 'uuid'])

class ClusterModel():
    def __init__(self):
        "Initialize model"

    def load_weights(self, name):
        self.model.load_weights(name)

    def name(self):
        return 'tsk-cluster'

    def train(self, epochs=20, patience=3):
        self.epochs = epochs
        self.patience = patience

        logging.info('Splitting train/val/test data...')
        (vector_train, vector_test, cluster_train,
         cluster_test) = data.data_split()
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

        inputs = Input(shape=(DEFAULT_SVD_COMPONENTS, ))

        outputs = pipe(inputs, Dense(uuid_count, activation='softmax'))

        _model = keras.models.Model(inputs=inputs, outputs=outputs)

        optimizer = Adam()

        _model.compile(
            loss='categorical_crossentropy',
            optimizer=optimizer,
            metrics=['categorical_accuracy'])

        return _model

    def predict(self, text, n_max=5):
        """Predicts clusters of TSK cross-references based on verse-like text

        Returns:

           list of (probability, cluster_id) tuples
        """
        result = self.model.predict(data.tokenize([text]))

        print(result.shape)

        indices = utils.n_max_indices(result[0], n=n_max)

        probabilities = list(result[0][indices])

        chosen = np.zeros(result.shape, np.int)
        chosen[:, indices] = 1

        clusters = (data
                    .uuid_encoder()
                    .inverse_transform(utils.categories_to_selections(chosen))
                    .reshape(1, -1)[0])

        return list_map(lambda x: ClusterResult(*x), zip(probabilities, clusters))

    def predict_repl(self, text, n_max):
        predicted = self.predict(text, n_max)

        uuids_to_passages = lens.Each()[1].modify(
                compose(list_map(lambda p: p.name), tsk.passages_by_uuid))

        return uuids_to_passages(predicted)

    def callbacks(self):
        return [
            ModelCheckpoint(
                os.path.join(CHECKPOINTS_PATH,
                             f'{self.name()}-{self.uuid}.hdf5'),
                save_best_only=True),
            EarlyStopping(patience=self.patience)
        ]

    def evaluate(self):
        print('Evaluating...')
        scores = self.model.evaluate(self.vector_test, self.cluster_test)
        print(f'Accuracy {scores[1] * 100:.2f}%')
