from ecce.model.ecce import EcceModel

def describe_model():

    def sanity_check():
        model = EcceModel(
            'ecce/data/checkpoints/lstm-f40827.hdf5',
            'ecce/data/checkpoints/tsk-cluster-52d4e6.hdf5')
        result = model.predict('God does not need our approval for his decisions.')

        assert len(result.topics) > 0
        assert len(result.clusters) > 0

