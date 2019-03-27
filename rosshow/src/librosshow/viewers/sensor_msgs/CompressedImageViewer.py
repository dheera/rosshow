import io
import numpy as np
import time
import PIL.Image
import librosshow.termgraphics as termgraphics

try:
    import PIL
except ImportError:
    print("This message type requires an additional Python package. Please run:")
    print("  $ sudo pip3 install pillow")
    print("and try again.")
    exit()

class CompressedImageViewer(object):
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

        current_image_obj = PIL.Image.open(io.BytesIO(self.msg.data))

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

        self.g.set_color((0, 127, 255))
        self.g.text(self.title, (0, self.g.shape[1] - 4))
        self.g.draw()
        self.last_update_time = time.time()
