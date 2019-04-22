import keras.models
from keras.layers import *
from keras.layers.embeddings import Embedding
from keras.optimizers import *
from toolz import memoize, pipe

import ecce.model.nave.data as data
from ecce.model.nave.model import Model


class LstmModel(Model):
    def name(self):
        return 'lstm'

    @property
    @memoize
    def model(self):
        embedding_matrix = data.embedding_matrix()
        word_count = embedding_matrix.shape[0]
        embedding_size = embedding_matrix.shape[1]
        max_length = data._text_tokenizer().num_words
        topic_count = len(data.topic_chunk_encoder().classes_)

        inputs = Input(shape=(max_length, ))

        outputs = pipe(
            inputs,
            Embedding(
                word_count,
                embedding_size,
                weights=[embedding_matrix],
                input_length=max_length,
                mask_zero=True),
            LSTM(800),
            Dense(topic_count * 3, activation='relu'),
            Dropout(0.2),
            Dense(topic_count, activation='sigmoid'))

        _model = keras.models.Model(inputs=inputs, outputs=outputs)

        optimizer = Adam()

        _model.compile(
            loss='categorical_crossentropy',
            optimizer=optimizer,
            metrics=['categorical_accuracy'])

        return _model
