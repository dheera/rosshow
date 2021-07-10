import numpy as np
import time

import librosshow.termgraphics as termgraphics
from librosshow.viewers.generic.Space2DViewer import Space2DViewer

class PathViewer(Space2DViewer):
    def __init__(self, canvas, title = ""):
        def msg_decoder(msg):
            """
            Calculates (x,y) coordinates from a Path message and returns them as a Nx2 numpy array.
            """

            points = np.array([[pose.pose.position.x, pose.pose.position.y] for pose in msg.poses], dtype = np.float64)

            draw_commands = [
                (Space2DViewer.COMMAND_TYPE_LINE,
                    termgraphics.COLOR_RED,
                    [(0., 0.), (1., 0.)]),
                (Space2DViewer.COMMAND_TYPE_LINE,
                    termgraphics.COLOR_GREEN,
                    [(0., 0.), (0., 1.)]),
                (Space2DViewer.COMMAND_TYPE_POINTS,
                    termgraphics.COLOR_WHITE,
                    points),
            ]

            if not self.init_centered and points.shape[0] > 0: 
                self.offset_x = points[0][0]
                self.offset_y = points[0][1]
                self.target_offset_x = points[0][0]
                self.target_offset_y = points[0][1]
                self.init_centered = True

            return draw_commands

        self.init_centered = False

        Space2DViewer.__init__(self, canvas, msg_decoder = msg_decoder, title = title)


