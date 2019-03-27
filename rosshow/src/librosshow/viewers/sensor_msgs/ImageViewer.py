import numpy as np
import time
import PIL.Image
import librosshow.termgraphics as termgraphics

class ImageViewer(object):
    def __init__(self, canvas, title = ""):
        self.g = canvas
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
            current_image = np.frombuffer(self.image.data, np.uint8).reshape((self.image.height, self.image.width, 3))[:, :, ::-1]
        elif self.image.encoding == 'rgb8':
            current_image = np.frombuffer(self.image.data, np.uint8).reshape((self.image.height, self.image.width, 3))
        elif self.image.encoding == 'mono8' or self.image.encoding == '8UC1':
            current_image = np.frombuffer(self.image.data, np.uint8).reshape((self.image.height, self.image.width))
            current_image = np.array((current_image.T, current_image.T, current_image.T)).T
        elif self.image.encoding == 'mono16' or self.image.encoding == '16UC1':
            current_image = np.frombuffer(self.image.data, np.uint16).reshape((self.image.height, self.image.width)).astype(np.float)
            current_image_max = np.percentile(current_image, 95)
            current_image_min = np.percentile(current_image, 5)
            current_image = 255*((current_image - current_image_min)/(current_image_max - current_image_min))
            current_image = np.clip(current_image, 0, 255) #.astype(np.uint8)
            current_image = np.array((current_image.T, current_image.T, current_image.T)).T
        else:
            print("Image encoding " + self.image.encoding + " not supported yet.")
            return

        current_image_obj = PIL.Image.fromarray(current_image.astype(np.uint8))

        image_ratio = 0.5 * float(current_image_obj.size[1]) / current_image_obj.size[0] # height / width
        terminal_ratio = 0.5 * float(h) / w  # height / width

        if image_ratio > terminal_ratio:
           target_image_height = int(h / 4.0)
           target_image_width = int(target_image_height / image_ratio)
        else:
           target_image_width = int(w / 2.0)
           target_image_height = int(image_ratio * target_image_width)

        resized_image_obj = current_image_obj.resize((target_image_width, target_image_height), PIL.Image.BILINEAR)
        resized_image = np.fromstring(resized_image_obj.tobytes(), dtype = np.uint8).reshape(target_image_width, target_image_height, 3)

        self.g.image(resized_image, target_image_width, target_image_height, (0, 0), image_type = termgraphics.IMAGE_RGB_2X4)

        if self.title:
            self.g.set_color((0, 127, 255))
            self.g.text(self.title, (0, self.g.shape[1] - 4))

        self.g.draw()
        self.last_update_time = time.time()
