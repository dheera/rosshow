#!/usr/bin/env python3

import numpy
import time
import scipy.misc

import librosshow.termgraphics as termgraphics

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
            current_image = numpy.frombuffer(data.data, numpy.uint8).reshape((data.height, data.width, 3))[:, :, ::-1]
        elif data.encoding == 'rgb8':
            current_image = numpy.frombuffer(data.data, numpy.uint8).reshape((data.height, data.width, 3))
        elif data.encoding == 'mono8' or data.encoding == '8UC1':
            current_image = numpy.frombuffer(data.data, numpy.uint8).reshape((data.height, data.width))
            current_image = numpy.array((current_image.T, current_image.T, current_image.T)).T
        elif data.encoding == 'mono16' or data.encoding == '16UC1':
            current_image = numpy.frombuffer(data.data, numpy.uint16).reshape((data.height, data.width)).astype(numpy.float)
            current_image_max = numpy.percentile(current_image, 95)
            current_image_min = numpy.percentile(current_image, 5)
            current_image = 255*((current_image - current_image_min)/(current_image_max - current_image_min))
            current_image = numpy.clip(current_image, 0, 255) #.astype(numpy.uint8)
            current_image = numpy.array((current_image.T, current_image.T, current_image.T)).T
        else:
            print("Image encoding " + data.encoding + " not supported yet.")
            return

        ratio = data.width / data.height
        if w/h * 4/2>= ratio:
           w = h * ratio
        else:
           h = w / ratio

        w = int(w/4)
        h = int(h/2)
        #w = int(w/7)
        #h = int(h/2)
        resized_image = list(map(tuple, scipy.misc.imresize(current_image, (w, h)).reshape((w*h, 3))))

        self.g.image(resized_image, h, w, (0, 0), image_type = termgraphics.IMAGE_RGB_2X4)
        self.g.draw()
        self.last_update_time = time.time()
