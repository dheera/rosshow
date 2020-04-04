import numpy as np

import librosshow.termgraphics as termgraphics
from librosshow.viewers.generic.GenericImageViewer import GenericImageViewer

class ImageViewer(GenericImageViewer):
    def __init__(self, canvas, title = ""):
        def msg_decoder(msg):
            """
            Decodes a sensor_msgs/Image ROS message into a numpy H x W x 3 RGB image.
            This basically reproduces what cv_bridge does (except to RGB instead of BGR),
            but cv_bridge doesn't support python3 :-/
            """

            if msg.encoding == 'bgr8':
                image = np.frombuffer(msg.data, np.uint8).reshape((msg.height, msg.width, 3))[:, :, ::-1]
            elif msg.encoding == 'rgb8':
                image = np.frombuffer(msg.data, np.uint8).reshape((msg.height, msg.width, 3))
            elif msg.encoding == 'mono8' or msg.encoding == '8UC1':
                image = np.frombuffer(msg.data, np.uint8).reshape((msg.height, msg.width))
                image = np.stack((image,) * 3, axis = -1) # greyscale to RGB
            elif msg.encoding == 'mono16' or msg.encoding == '16UC1':
                image = np.frombuffer(msg.data, np.uint16).reshape((msg.height, msg.width)).astype(np.float)
                image_max = np.percentile(image, 95)
                image_min = np.percentile(image, 5)
                image = 255*((image - image_min)/(image_max - image_min))
                image = np.clip(image, 0, 255)
                image = np.stack((image,) * 3, axis = -1) # greyscale to RGB
            else:
                print("Image encoding " + msg.encoding + " not supported yet.")
                return None

            return image

        GenericImageViewer.__init__(self, canvas, msg_decoder = msg_decoder, title = title)

