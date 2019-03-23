import io
import numpy as np
import time
import scipy.misc

try:
    import PIL
except ImportError:
    print("This message type requires an additional Python package. Please run:")
    print("  $ sudo pip3 install pillow")
    print("and try again.")
    exit()

import librosshow.termgraphics as termgraphics

class CompressedImageViewer(object):
    def __init__(self):
        self.g = termgraphics.TermGraphics()
        self.xmax = 20
        self.ymax = 20
        self.last_update_time = 0
        self.msg = None

    def update(self, msg):
        self.msg = msg

    def draw(self):
        if not self.msg:
            return

        self.g.clear()
        w = self.g.shape[0]
        h = self.g.shape[1]

        current_image_obj = PIL.Image.open(io.BytesIO(self.msg.data))

        current_image = np.fromstring(current_image_obj.tobytes(), dtype=np.uint8)
        current_image = current_image.reshape((current_image_obj.size[1], current_image_obj.size[0], 3))    

        ratio = float(current_image.shape[0]) / current_image.shape[1]
        if float(w)/float(h) * 2.0>= ratio:
           w = float(h) * ratio
        else:
           h = float(w) / ratio

        w = int(w/4.0)
        h = int(h/2.0)
        resized_image = list(map(tuple, scipy.misc.imresize(current_image, (w, h)).reshape((w*h, 3))))

        self.g.image(resized_image, h, w, (0, 0), image_type = termgraphics.IMAGE_RGB_2X4)
        self.g.draw()
        self.last_update_time = time.time()
