import numpy as np
import time

import librosshow.termgraphics as termgraphics
from librosshow.viewers.generic.Space2DViewer import Space2DViewer

class LaserScanViewer(Space2DViewer):
    def __init__(self, canvas, title = ""):
        def msg_decoder(msg):
            """
            Calculates (x,y) coordinates from a LaserScan message and returns them as a Nx2 numpy array.
            """
            angles = np.linspace(self.msg.angle_min, self.msg.angle_max, len(self.msg.ranges), dtype = np.float32)
            ranges = np.array(self.msg.ranges, dtype = np.float32)
            x_values = ranges * np.cos(angles)
            y_values = ranges * np.sin(angles)

            draw_commands = [
                (Space2DViewer.COMMAND_TYPE_LINE,
                    termgraphics.COLOR_RED,
                    [(0., 0.), (1., 0.)]),
                (Space2DViewer.COMMAND_TYPE_LINE,
                    termgraphics.COLOR_GREEN,
                    [(0., 0.), (0., 1.)]),
                (Space2DViewer.COMMAND_TYPE_POINTS,
                    termgraphics.COLOR_WHITE,
                    np.vstack((x_values, y_values)).T),
            ]

            return draw_commands

        Space2DViewer.__init__(self, canvas, msg_decoder = msg_decoder, title = title)


