from functools import lru_cache
import io

from PIL import Image
import numpy as np


def convert(filename, threshold=None):
    """
    """
    BYTE_SIZE = 8
    WIDTH = 128
    HEIGHT = 64
    end = 8
    start = 0

    img = Image.open(filename).resize((WIDTH, HEIGHT))
    if threshold is None:
        img = img.convert('1', dither=Image.NONE)
    else:
        img = img.convert('L')
        img = img.point(lambda x: 255 if x > int(threshold) else 0)
        img.convert('1')
    arr = np.array(img, dtype=int)

    bytelist = []

    for row in range(HEIGHT):
        # Divide row of 128 pixels into 8 bit chunks
        # In a row of 128 columns there is exactly 16 8-byte chunks so
        # hardcoding '16' here instead of using arithmetic or variable
        for col in range(16):
            if threshold is not None:
                arr[row][arr[row] == 255] = 1
            bits = ''.join(str(bit) for bit in arr[row][start:end])
            bits = hex(int(bits, 2))
            bytelist.append(bits)
            start = end
            end += 8
        start = 0
        end = 8

    img.close()

    return ','.join(bit for bit in bytelist)


def resize(filename):
    from PySide2 import QtGui

    img = Image.open(filename)
    img_resized = img.resize((128, 64))
    img_onebit = img_resized.convert('1', dither=Image.NONE)
    img_bytes = io.BytesIO()
    img_onebit.save(img_bytes, format=img.format)
    qimg = QtGui.QImage()
    qimg.loadFromData(img_bytes.getvalue())
    pixmap = QtGui.QPixmap(qimg)
    img.close()
    return pixmap
