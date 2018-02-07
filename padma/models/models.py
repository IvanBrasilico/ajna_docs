from keras.applications import ResNet50, imagenet_utils
from models.vazios.vazios import NaiveModel, RetinaModel, VazioModel


class ModelBase():
    def __init__(self):
        self._model = None
        self._preds = {}

    def predict(self, data):
        if not self._model:
            raise('Error! Model not assigned.')
        self._preds = self._model.predict(data)
        return self._preds

    def format(self, preds):
        return preds


class ResNet(ModelBase):
    def __init__(self, weights='imagenet'):
        self._model = ResNet50(weights=weights)

    def format(self, preds):
        result_set = imagenet_utils.decode_predictions(preds)
        output = []
        for (_, label, prob) in result_set[0]:
            output.append({'label': label, 'probability': float(prob)})
        return output


class Vazios(ModelBase):
    def __init__(self):
        self._model = VazioModel()

#    def predict(self, data):
#        self._preds = {'0': 0.99, '1': 0.01}
#        return self._preds

class Retina(ModelBase):
    def __init__(self):
        self._model = RetinaModel()


class Naive(ModelBase):
    def __init__(self):
        self._model = NaiveModel()
