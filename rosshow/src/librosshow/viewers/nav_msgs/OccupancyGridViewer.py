import numpy as np
import time
import PIL.Image
import librosshow.termgraphics as termgraphics

class OccupancyGridViewer(object):
    def __init__(self, canvas, title = ""):
        self.g = canvas
        self.xmax = 20
        self.ymax = 20
        self.last_update_time = 0
        self.msg = None
        self.title = title
        self.last_update_shape_time = 0

    def update(self, msg):
        self.msg = msg

    def draw(self):
        if not self.msg:
            return

        t = time.time()

        # capture changes in terminal shape at least every 0.25s
        if t - self.last_update_shape_time > 0.25:
            self.g.update_shape()
            self.last_update_shape_time = t

        self.g.clear()
        w = self.g.shape[0]
        h = self.g.shape[1]

        occupancy_map = np.array(self.msg.data)
        occupancy_map = occupancy_map.reshape(self.msg.info.height, self.msg.info.width)


        color_prob_zero = np.array([0, 0, 0], dtype=np.uint8)
        color_prob_one = np.array([255, 255, 255], dtype=np.uint8)

        map_image = ((100 - occupancy_map).astype(np.float16) * (255.0 / 100.0)).astype(np.uint8)
        map_image = np.stack((map_image,)*3, axis = -1) # greyscale to rgb

        # display <0 in yellow
        map_image[occupancy_map < 0] = [255, 127, 0]

        # display >100 in red
        map_image[occupancy_map > 100] = [255, 0, 0]

        current_image_obj = PIL.Image.fromarray(map_image.astype(np.uint8))

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
