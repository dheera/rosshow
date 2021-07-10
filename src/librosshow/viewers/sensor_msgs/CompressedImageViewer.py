import io
import numpy as np
import sys

import librosshow.termgraphics as termgraphics
from librosshow.viewers.generic.GenericImageViewer import GenericImageViewer

try:
    import PIL.Image
except ImportError:
    print("Viewing sensor_msgs/CompressedImage requires the PIL package. Please run:")
    three = ""
    if sys.version_info[0] == 3:
        three = "3"
    print("  $ sudo pip%s install pillow" % three)
    print("or")
    print("  $ sudo apt install python%s-pil" % three)
    print("and try again.")
    exit(1)

class CompressedImageViewer(GenericImageViewer):
    def __init__(self, canvas, title = ""):
        def msg_decoder(msg):
            """
            Decodes a sensor_msgs/CompressedImage ROS message into a numpy H x W x 3 RGB image.
            Using PIL to decode compressed images because ROS's cv2 doesn't have python3 bindings.
            TODO: Make a version that can gracefully use either PIL.Image.open() or cv2.imdecode() depending
            on what is available.
            """

            image_obj = PIL.Image.open(io.BytesIO(self.msg.data))
            if image_obj.mode != "RGB":
                image_obj = image_obj.convert("RGB")
            return image_obj

        GenericImageViewer.__init__(self, canvas, msg_decoder = msg_decoder, title = title)

