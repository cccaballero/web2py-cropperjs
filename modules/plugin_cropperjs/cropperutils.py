from PIL import Image
from io import BufferedRandom
from io import BytesIO
import logging
from gluon import current
import re

logger = logging.getLogger(current.request.application)


def to_int(string):
    """
    Convert a string to integer
    :param str string: A number in string format
    :return: the string as integer
    :rtype str
    """
    return int(float(string))


def crop_image(file_object, x, y, w, h, rotate):
    """
    Crop a file request Storage object and return it in png format
    :param gluon.storage.Storage file_object: File request Storage object
    :param str x: Cropper X position
    :param str y: Cropper Y position
    :param str w: Cropper image width
    :param str h: Cropper image height
    :param str rotate: Cropper rotate value
    :return: File request Storage object
    :rtype: gluon.storage.Storage
    """
    logger.debug("start cropping image")
    image = file_object.file
    image_filename = file_object.filename

    try:
        logger.debug("Opening request image")
        im = Image.open(image).convert('RGBA')
    except Exception as e:
        logger.error(e)
        return file_object

    logger.debug("Request image open")

    if rotate:
        img_tempfile = im.rotate(-to_int(rotate), expand=True)
        logger.debug("Image rotated")
    else:
        img_tempfile = im
    img_tempfile = img_tempfile.crop((to_int(x), to_int(y), to_int(w)+to_int(x), to_int(h)+to_int(y)))
    logger.debug("Image cropped")
    tempfile_io = BytesIO()
    img_tempfile.save(tempfile_io, format='PNG')
    tempfile_io.seek(0)
    tempfile_io = BufferedRandom(tempfile_io)
    logger.debug("Image saved to buffer")

    logger.debug("Image cropping finished")

    file_object.file = tempfile_io
    file_object.filename = '.'.join(image_filename.split('.')[:-1]) + ".png"
    logger.debug("New image file object builded")
    return file_object


def camel_to_lisp(text):
    """
    Convert camelCase string to lisp-case
    :param str text: A camel case string
    :return: Same input text using list-case format
    :rtype: str
    """
    str1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', str1).lower()
