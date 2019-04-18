import numpy as np

import ecce.tsk as tsk
import ecce.modeling.tsk.data as data

def describe_tsk():

    def describe_uuid_encoding():

        def matches():
            uuid = data.bag_of_words(tsk.init())[4][0]
            encoder = data.uuid_encoder()

            assert encoder.inverse_transform(encoder.transform([[uuid]])) == uuid

    def describe_tokenize():

        def converts_to_numpy_array():
            vector = data.tokenize(['what is life', 'overflow of the heart'])
            assert vector.shape == (2, 100)
