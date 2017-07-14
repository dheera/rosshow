#!/usr/bin/env python3

import numpy
import time
import scipy.misc

from . import termgraphics

class ImageViewer(object):
    def __init__(self):
        self.g = termgraphics.TermGraphics()
        self.xmax = 20
        self.ymax = 20
        self.last_update_time = 0

    def update(self, data):
        if time.time() - self.last_update_time < 0.075:
            return

        self.g.clear()
        w = self.g.shape[0]
        h = self.g.shape[1]
        if data.encoding == 'bgr8':
            current_image = numpy.fromstring(data.data, numpy.uint8).reshape((data.height, data.width, 3))[:, :, ::-1]
        elif data.encoding == 'rgb8':
            current_image = numpy.fromstring(data.data, numpy.uint8).reshape((data.height, data.width, 3))
        else:
            print("Image encoding not supported yet.")
            return

        ratio = data.width / data.height
        if w/h >= ratio:
           w = h * ratio
        else:
           h = w / ratio

        w = int(w/7)
        h = int(h/2)

        resized_image = list(map(tuple, scipy.misc.imresize(current_image, (w, h)).reshape((w*h, 3))))

        self.g.image(resized_image, h, w, (0, 0), image_type = termgraphics.IMAGE_RGB_2X4)
        self.g.draw()
        self.last_update_time = time.time()
