import numpy as np
import time

import librosshow.termgraphics as termgraphics
from librosshow.viewers.generic.Space2DViewer import Space2DViewer

class OdometryViewer(Space2DViewer):
    def __init__(self, canvas, title = ""):
        def msg_decoder(msg):
            """
            Calculates (x,y) coordinates from a Odometry message and returns them as a Nx2 numpy array.
            """

            self.points[self.points_i][0] = msg.pose.pose.position.x
            self.points[self.points_i][1] = msg.pose.pose.position.y
            self.points_i = (self.points_i + 1) & 0xFF # mod 256

            draw_commands = [
                (Space2DViewer.COMMAND_TYPE_LINE,
                    termgraphics.COLOR_RED,
                    [(0., 0.), (1., 0.)]),
                (Space2DViewer.COMMAND_TYPE_LINE,
                    termgraphics.COLOR_GREEN,
                    [(0., 0.), (0., 1.)]),
                (Space2DViewer.COMMAND_TYPE_POINTS,
                    termgraphics.COLOR_WHITE,
                    self.points),
            ]

            if not self.init_centered: 
                self.offset_x = msg.pose.pose.position.x
                self.offset_y = msg.pose.pose.position.y
                self.target_offset_x = msg.pose.pose.position.x
                self.target_offset_y = msg.pose.pose.position.y
                self.init_centered = True

            # quaternion to euler
            norm = (msg.pose.pose.orientation.x ** 2 + msg.pose.pose.orientation.y ** 2 + msg.pose.pose.orientation.z ** 2 + msg.pose.pose.orientation.w ** 2) ** 0.5
            if norm != 0.:
                a = msg.pose.pose.orientation.x / norm
                b = msg.pose.pose.orientation.y / norm
                c = msg.pose.pose.orientation.z / norm
                d = msg.pose.pose.orientation.w / norm
                yaw = np.arctan2(2*a*b+2*c*d, 1-2*b*b-2*c*c)

                draw_commands.append((
                    Space2DViewer.COMMAND_TYPE_LINE,
                    (127, 127, 127),
                    [
                        (msg.pose.pose.position.x, msg.pose.pose.position.y),
                        (msg.pose.pose.position.x + np.cos(yaw), msg.pose.pose.position.y + np.sin(yaw))
                    ],
                ))

            return draw_commands

        self.points = np.empty((256, 2), dtype = np.float64)
        self.points[:,:] = np.nan
        self.points_i = 0
        self.init_centered = False

        Space2DViewer.__init__(self, canvas, msg_decoder = msg_decoder, title = title)


