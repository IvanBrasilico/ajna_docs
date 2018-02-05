"""Algoritmos para encontrar a borda dos contêineres
Recebem uma imagem, retornam as coordenadas de um retângulo
onde o contêiner está
bbox (x1, y1, x2, y2)"""


class RetinaModel():
    def __init__(self):
        import keras
        from keras_retinanet.models.resnet import custom_objects
        import os
        import tensorflow as tf
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        session = tf.Session(config=config)
        keras.backend.tensorflow_backend.set_session(session)
        model_path = os.path.join('resnet50_csv.h5')
        self._model = keras.models.load_model(
            model_path, custom_objects=custom_objects)
        self._labels_to_names = {0: 'cc'}

    def predict(self, image):
        import numpy as np
        from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
        image = preprocess_image(image)
        image, scale = resize_image(image)
        _, _, detections = self._model.predict_on_batch(
            np.expand_dims(image, axis=0))
        predicted_labels = np.argmax(detections[0, :, 4:], axis=1)
        scores = detections[0, np.arange(
            detections.shape[1]), 4 + predicted_labels]
        # correct for image scale
        detections[0, :, :4] /= scale
        # visualize detections
        result = []
        for idx, (label, score) in enumerate(zip(predicted_labels, scores)):
            if score < 0.5:
                continue
            b = detections[0, idx, :4].astype(int)
            caption = "{} {:.3f}".format(self._labels_to_names[label], score)
            result.append((b, caption))
        return result


def find_conteiner(afile):
    """Heuristic dumb walk algorithm
    Beginning on middle of top, left, right and bottom sizes,
    do a 'walk till find wall(gray>230)'.
    Besides simplicity, works well to find conteiner boundaries on majority of cases,
    so is a beggining and can acelerate anottations for training better algorithm

    Args:

    afile: caminho da imagem no disco

    Returns:

    xleft, ytop, xright, ybottom

    """
    im = afile[:, :, 0]
    yfinal, xfinal = im.shape
    ymeio = round(yfinal / 2)
    xmeio = round(xfinal / 2)
    # primeiro achar o Teto do contêiner. Tentar primeiro exatamente no meio
    yteto = 0
    for s in range(0, ymeio):
        if (im[s, xmeio] < 230):
            yteto = s
            break
    # Depois de achado o teto, percorrer as laterais para achar os lados
    xesquerda = 1
    for r in range(0, xmeio):
        if (im[yteto+5, r] < 230):
            xesquerda = r
            break
    xdireita = xfinal - 1
    for r in range(xfinal-1, xmeio, -1):
        if (im[yteto+5, r] < 215):
            xdireita = r
            break
    # Achar o piso do contêiner é bem mais difícil... Pensar em como fazer depois Talvez o ponto de max valores
    imbaixo = im[ymeio:yfinal, xesquerda:xdireita]
    ychao = imbaixo.sum(axis=1).argmin()
    ychao = ychao + ymeio + 10
    # Por fim, fazer umas correções se as medidas achadas forem absurdas
    if (ychao > yfinal):
        ychao = yfinal
    if ((xdireita-xesquerda) < (xfinal/4)):
        xdireita = xfinal - 5
        xesquerda = 5
    if (yteto == ymeio):
        yteto = 5
    return xesquerda, yteto, xdireita, ychao


class NaiveModel():

    def predict(self, image):
        # from image_aq.utils.image_functions import find_conteiner
        # Code copied from this file because of path problems
        # TODO: allow padma submodule import things from AJNA_MOD
        return((find_conteiner(image), 'cc'))
