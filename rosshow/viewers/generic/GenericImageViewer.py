import numpy as np
import time
import librosshow.termgraphics as termgraphics

try:
    import PIL.Image
except ImportError:
    print("Viewing images requires the PIL package. Please run:")
    three = ""
    if sys.version_info[0] == 3:
        three = "3"
    print("  $ sudo pip%s install pillow" % three)
    print("or")
    print("  $ sudo apt install python%s-pil" % three)
    print("and try again.")
    exit(1)

class GenericImageViewer(object):
    def __init__(self, canvas, msg_decoder = None, title = ""):
        self.g = canvas
        self.xmax = 20
        self.ymax = 20
        self.last_update_time = 0

        # Most recent ROS message
        self.msg = None

        # Last time terminal shape was updated
        self.last_update_shape_time = 0

        # Function that converts ROS message to a numpy RGB image OR PIL.Image to display (either is OK)
        self.msg_decoder = msg_decoder

        # Display title
        self.title = title

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

        image = self.msg_decoder(self.msg)


        if type(image) == np.ndarray: # we accept ndarray HxWx3 (RGB)
            if len(image.shape) != 3:
                print("GenericImageViewer error: expected shape (H,W,3)")
                exit(1)
            if image.shape[2] != 3:
                print("GenericImageViewer error: expected shape (H,W,3)")
                exit(1)

            image_obj = PIL.Image.fromarray(image.astype(np.uint8))

        elif PIL.Image.isImageType(image): # we accept PIL.Image
            if image.mode != "RGB":
                print("GenericImageViewer error: received non-RGB PIL image")
                exit(1)

            image_obj = image

        else: # complain
            print("GenericImageViewer error: received invalid image type %s" % str(type(image)))
            exit(1)

        image_ratio = 0.5 * float(image_obj.size[1]) / image_obj.size[0] # height / width
        terminal_ratio = 0.5 * float(h) / w  # height / width

        if image_ratio > terminal_ratio:
           target_image_height = int(h / 4.0)
           target_image_width = int(target_image_height / image_ratio)
        else:
           target_image_width = int(w / 2.0)
           target_image_height = int(image_ratio * target_image_width)

        resized_image_obj = image_obj.resize((target_image_width, target_image_height), PIL.Image.BILINEAR)
        resized_image = np.fromstring(resized_image_obj.tobytes(), dtype = np.uint8).reshape(target_image_width, target_image_height, 3)

        self.g.image(resized_image, target_image_width, target_image_height, (0, 0), image_type = termgraphics.IMAGE_RGB_2X4)

        if self.title:
            self.g.set_color((0, 127, 255))
            self.g.text(self.title, (0, self.g.shape[1] - 4))

        self.g.draw()
        self.last_update_time = time.time()
