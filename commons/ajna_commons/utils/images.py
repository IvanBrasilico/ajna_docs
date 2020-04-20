"""Funções para tratamento de imagens."""
import io
from PIL import Image, ImageDraw, ImageOps
from ajna_commons.flask.log import logger
from bson.objectid import ObjectId
from gridfs import GridFS


def bytes_toPIL(img: io.BytesIO) -> Image:
    return Image.open(img)

def PIL_tobytes(pil_image: Image) -> io.BytesIO:
    image_bytes = io.BytesIO()
    pil_image.save(image_bytes, 'JPEG')
    image_bytes.seek(0)
    return image_bytes


def recorta_imagem(image, coords, pil=False):
    """Recebe uma imagem serializada em bytes, retorna Imagem cortada.

    Params:
        image: imagem em bytes (recebida via http ou via Banco de Dados)
        coords: (x0,y0,x1,y1)
        pil: flag, retorna objeto PIL se True

    Returns:
        Um recorte da imagem em bytes ou formato PIL.Image se PIL=true

    """
    if isinstance(image, bytes):
        pil_image = Image.open(io.BytesIO(image))
    else:
        pil_image = image
    pil_image = pil_image.crop((coords[1], coords[0], coords[3], coords[2]))
    if pil:
        return pil_image
    return PIL_tobytes(pil_image)


def draw_bboxes(image_bytes: bytes, bboxes: list):
    pil_img = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(pil_img)
    for coords in bboxes:
        draw.rectangle((coords[1] - 2, coords[0] - 2, coords[3] + 2, coords[2] + 2),
                       outline='#2288EE', width=4)
        # image.draw()
    return PIL_tobytes(pil_img)


def mongo_image(db, image_id, bboxes=False):
    """Lê imagem do Banco MongoDB. Retorna None se ID não encontrado."""
    fs = GridFS(db)
    _id = ObjectId(image_id)
    if fs.exists(_id):
        grid_out = fs.get(_id)
        image = grid_out.read()
        if bboxes:
            predictions = grid_out.metadata.get('predictions')
            if predictions:
                bboxes = [pred.get('bbox') for pred in predictions]
                image = draw_bboxes(image, bboxes)
        return image
    return None


def get_imagens_recortadas(db, _id):
    """Retorna recorte das bbox detectadas para a imagem _id.

    Caso existam predições bbox gravadas/cacheadas nos metadados da
    imagem, retorna, ao invés da imagem original completa, apenas os
    recortes correspondentes a estes "bouding boxes" detectados.
    """
    images = []
    image = mongo_image(db, _id)
    if image:
        preds = db['fs.files'].find_one({'_id': _id}).get(
            'metadata').get('predictions')
        if preds:
            for pred in preds:
                bbox = pred.get('bbox')
                if bbox:
                    try:
                        recorte = recorta_imagem(image, bbox, pil=True)
                        images.append(recorte)
                    except Exception as err:
                        logger.info('Erro em get_imagens_recortadas ' +
                                    'Erro: %s\n bbox:%s\n imagem:%s' %
                                    (str(err), bbox, _id), exc_info=True)
    return images


def get_cursor(db, filtro, projection=None, limit=None):
    if projection:
        cursor = db['fs.files'].find(filtro, projection)
    else:
        cursor = db['fs.files'].find(filtro)
    if limit:
        cursor = cursor[:limit]
    return cursor


def generate_batch(db, filtro, projection=None, batch_size=32,
                   limit=None, recorta=True):
    """a generator for batches, so model.fit_generator can be used. """
    cursor = get_cursor(db, filtro, projection, limit)
    while True:
        images = []
        rows = []
        i = 0
        while i < batch_size:
            try:
                row = next(cursor)
            except StopIteration:
                break
            if recorta:
                imgs = get_imagens_recortadas(db, row['_id'])
            else:
                imgs = [Image.open(io.BytesIO(mongo_image(db, row['_id'])))]
            images.append(imgs)
            rows.append(row)
            i += 1
        yield images, rows


class ImageBytesTansFormations:

    @classmethod
    def get_tranformation(cls, name):
        return getattr(cls, name)

    @classmethod
    def get_available_transformations(cls):
        return [method for method in dir(cls) if '_' not in method]

    @classmethod
    def rotate90(cls, image_bytes):
        pil_img = Image.open(io.BytesIO(image_bytes))
        pil_img = pil_img.transpose(Image.ROTATE_90)
        return PIL_tobytes(pil_img)

    @classmethod
    def rotate270(cls, image_bytes):
        pil_img = Image.open(io.BytesIO(image_bytes))
        pil_img = pil_img.transpose(Image.ROTATE_270)
        return PIL_tobytes(pil_img)

    @classmethod
    def equalize(cls, image_bytes):
        pil_img = Image.open(io.BytesIO(image_bytes))
        pil_img = ImageOps.equalize(pil_img)
        return PIL_tobytes(pil_img)


    @classmethod
    def crop10(cls, image_bytes):
        pil_img = Image.open(io.BytesIO(image_bytes))
        pil_img = ImageOps.crop(pil_img, int(pil_img.size[0] / 10))
        return PIL_tobytes(pil_img)
