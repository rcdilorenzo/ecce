import keras.models
from keras.layers import *
from keras.layers.embeddings import Embedding
from keras.optimizers import *
from toolz import memoize, pipe

import ecce.modeling.data as data
from ecce.modeling.model import Model


class GruModel(Model):
    def name(self):
        return 'gru'

    @property
    @memoize
    def model(self):
        embedding_matrix = data.embedding_matrix()
        word_count = embedding_matrix.shape[0]
        embedding_size = embedding_matrix.shape[1]
        max_length = data._text_tokenizer().num_words
        topic_count = len(data.topic_encoder().classes_)

        inputs = Input(shape=(max_length, ))

        outputs = pipe(
            inputs,
            Embedding(
                word_count,
                embedding_size,
                weights=[embedding_matrix],
                input_length=max_length,
                mask_zero=True),
            BatchNormalization(),
            GRU(200),
            Dense(topic_count, activation='sigmoid'),
            Dense(topic_count, activation='sigmoid'))

        _model = keras.models.Model(inputs=inputs, outputs=outputs)

        optimizer = Adam()

        _model.compile(
            loss='categorical_crossentropy',
            optimizer=optimizer,
            metrics=['categorical_accuracy'])

        return _model
