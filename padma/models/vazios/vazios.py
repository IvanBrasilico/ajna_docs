# -*- coding: utf-8 -*-
import pickle
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from scipy import misc


class VazioModel():
    def __init__(self, bins=32):
        self._bins = bins
        histograms = pickle.load(
            open(os.path.join(os.path.dirname(__file__),
                              'histograms.pkl'), "rb"))
        labels = pickle.load(
            open(os.path.join(os.path.dirname(__file__),
                              'labels.pkl'), "rb"))
        self.clf = RandomForestClassifier()
        self.clf.fit(histograms, labels)

    def hist(self, img):
        histo = np.histogram(img, bins=self._bins, density=True)
        return histo[0]

    def vaziooucheio(self, file=None, image=None):
        if file:
            image = misc.imread(file)
        return self.clf.predict_proba([self.hist(image)])

    def vaziooucheiodescritivo(self, file=None, image=None):
        teste = self.vaziooucheio(file=file, image=image)
        if teste[0][0] > 0.5:
            return "Contêiner avaliado como VAZIO"
        else:
            return "Contêiner avaliado como NÃO VAZIO"
    
    def predict(self, image):
        probs = self.vaziooucheio(image=image)
        result = []
        for vazio, cheio in probs:
            item = {}
            item['0'] = vazio
            item['1'] = cheio
            result.append(item)
        return result

