import base64
import numpy as np
from keras.applications import imagenet_utils
from keras.preprocessing.image import img_to_array


def base64_encode_image(a):
    # base64 encode the input NumPy array
    return base64.b64encode(a).decode('utf-8')


def base64_decode_image(a, dtype, shape):
    # if this is Python 3, we need the extra step of encoding the
    # serialized NumPy string as a byte object
    a = bytes(a, encoding='utf-8')

    # convert the string to a NumPy array using the supplied data
    # type and target shape
    a = np.frombuffer(base64.decodestring(a), dtype=dtype)
    a = a.reshape(shape)

    # return the decoded image
    return a


def prepare_image(image, target):
    # if the image mode is not RGB, convert it
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # resize the input image and preprocess it
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # return the processed image
    return image
