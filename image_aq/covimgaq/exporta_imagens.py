import datetime
import os

from image_aq.models.bsonimage import BsonImage, BsonImageList

IMG_FOLDER = os.path.join(__file__, '..', '..', 'padma/tests/')
DEST_PATH = ''

# TODO: Ver no AJNA informações que serão lançadas no arquivo



def exportadir():
    bsonimagelist = BsonImageList()
    for file in os.listdir(IMG_FOLDER):
        bsonimage = BsonImage(
            filename=os.path.join(IMG_FOLDER, file),
            chave='MSKU123',
            origem=0,
            data=datetime.datetime.utcnow()
        )
        bsonimagelist.addBsonImage(bsonimage)
    bsonimagelist.tofile(os.path.join(DEST_PATH, 'list.bson'))
