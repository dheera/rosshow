import numpy
import time
import scipy.misc

import librosshow.termgraphics as termgraphics

class ImageViewer(object):
    def __init__(self, title = ""):
        self.g = termgraphics.TermGraphics()
        self.xmax = 20
        self.ymax = 20
        self.last_update_time = 0
        self.image = None
        self.title = title
        self.last_update_shape_time = 0

    def update(self, msg):
        self.image = msg

    def draw(self):
        if not self.image:
            return

        t = time.time()

        # capture changes in terminal shape at least every 0.25s
        if t - self.last_update_shape_time > 0.25:
            self.g.update_shape()
            self.last_update_shape_time = t

        self.g.clear()
        w = self.g.shape[0]
        h = self.g.shape[1]
        if self.image.encoding == 'bgr8':
            current_image = numpy.frombuffer(self.image.data, numpy.uint8).reshape((self.image.height, self.image.width, 3))[:, :, ::-1]
        elif self.image.encoding == 'rgb8':
            current_image = numpy.frombuffer(self.image.data, numpy.uint8).reshape((self.image.height, self.image.width, 3))
        elif self.image.encoding == 'mono8' or self.image.encoding == '8UC1':
            current_image = numpy.frombuffer(self.image.data, numpy.uint8).reshape((self.image.height, self.image.width))
            current_image = numpy.array((current_image.T, current_image.T, current_image.T)).T
        elif self.image.encoding == 'mono16' or self.image.encoding == '16UC1':
            current_image = numpy.frombuffer(self.image.data, numpy.uint16).reshape((self.image.height, self.image.width)).astype(numpy.float)
            current_image_max = numpy.percentile(current_image, 95)
            current_image_min = numpy.percentile(current_image, 5)
            current_image = 255*((current_image - current_image_min)/(current_image_max - current_image_min))
            current_image = numpy.clip(current_image, 0, 255) #.astype(numpy.uint8)
            current_image = numpy.array((current_image.T, current_image.T, current_image.T)).T
        else:
            print("Image encoding " + self.image.encoding + " not supported yet.")
            return

        image_ratio = 0.5 * float(current_image.shape[0]) / current_image.shape[1] # height / width
        terminal_ratio = 0.5 * float(h) / w  # height / width

        if image_ratio > terminal_ratio:
           target_image_height = int(h / 4.0)
           target_image_width = int(target_image_height / image_ratio)
        else:
           target_image_width = int(w / 2.0)
           target_image_height = int(image_ratio * target_image_width)

        resized_image = list(map(tuple, scipy.misc.imresize(current_image, \
                (target_image_height, target_image_width)).reshape((target_image_width * target_image_height, 3))))

        self.g.image(resized_image, target_image_width, target_image_height, (0, 0), image_type = termgraphics.IMAGE_RGB_2X4)

        if self.title:
            self.g.set_color((0, 127, 255))
            self.g.text(self.title, (0, self.g.shape[1] - 4))

        self.g.draw()
        self.last_update_time = time.time()
