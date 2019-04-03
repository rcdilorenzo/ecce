import ecce.modeling.data as data


class Model():
    def __init__(self):
        (text_train, text_test, topics_train, topics_test) = data.data_split()
        self.text_train = text_train
        self.text_test = text_test
        self.topics_train = topics_train
        self.topics_test = topics_test

    def train(self):
        print('Training...')
        self.model.summary()

        self.model.fit(
            self.text_train,
            self.topics_train,
            epochs=50,
            batch_size=256,
            validation_split=0.15)

    def evaluate(self):
        print('Evaluating...')
        scores = self.model.evaluate(self.text_test, self.topics_test)
        print(f'Accuracy {scores[1] * 100:.2f}%')

    @property
    def model(self):
        return None
