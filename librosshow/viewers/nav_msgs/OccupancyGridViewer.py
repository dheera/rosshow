import numpy as np
import time
import PIL.Image
import librosshow.termgraphics as termgraphics

from librosshow.viewers.generic.GenericImageViewer import GenericImageViewer

class OccupancyGridViewer(GenericImageViewer):
    def __init__(self, canvas, title = ""):
        def msg_decoder(msg):
            """
            Decodes a nav_msgs/OccupancyGrid ROS message into a numpy H x W x 3 RGB visualization.
            Values <0 are shown in yellow
            Values >100 are shown in red
            0-100 are probabilities and shown as white to black
            """

            occupancy_map = np.array(self.msg.data, dtype=np.int16).reshape(self.msg.info.height, self.msg.info.width)[::-1, :]

            color_prob_zero = np.array([0, 0, 0], dtype=np.uint8)
            color_prob_one = np.array([255, 255, 255], dtype=np.uint8)

            map_image = ((100 - occupancy_map) * 10 // 4).astype(np.uint8) # *10//4 is int approx to *255.0/100.0
            map_image = np.stack((map_image,)*3, axis = -1) # greyscale to rgb

            # display <0 in yellow
            map_image[occupancy_map < 0] = [255, 127, 0]

            # display >100 in red
            map_image[occupancy_map > 100] = [255, 0, 0]

            return map_image

        GenericImageViewer.__init__(self, canvas, msg_decoder = msg_decoder, title = title)

