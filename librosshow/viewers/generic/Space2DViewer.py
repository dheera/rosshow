import numpy as np
import time

import librosshow.termgraphics as termgraphics

class Space2DViewer(object):
    """
    A generic zoomable/pannable 2D point/line viewer. Requires a msg_decoder
    callback function that converts given ROS message into a sequence of points/lines
    to plot.
    """

    def __init__(self, canvas, msg_decoder = None, title = "", offset_x = 0.0, offset_y = 0.0, scale = 10.0):
        # A TermGraphics canvas to draw on
        self.canvas = canvas
        
        # Viewer geometry
        self.scale = scale
        self.offset_x = offset_x
        self.offset_y = offset_y

        # Animation targets for viewer geometry
        self.target_scale = scale
        self.target_offset_x = offset_x
        self.target_offset_y = offset_y
        self.target_time = 0

        # Most recent ROS message
        self.msg = None

        # Last time terminal shape was updated
        self.last_update_shape_time = 0

        # Function that converts ROS message to Nx2 point array
        self.msg_decoder = msg_decoder

        # Display title
        self.title = title

    def keypress(self, c):
        if c == "+" or c == "=":
            self.target_scale /= 1.5
            self.target_time = time.time()
        elif c == "-":
            self.target_scale *= 1.5
            self.target_time = time.time()
        elif c == "up":
            self.target_offset_y += self.scale / 10
            self.target_time = time.time()
        elif c == "down":
            self.target_offset_y -= self.scale / 10
            self.target_time = time.time()
        elif c == "left":
            self.target_offset_x += self.scale / 10
            self.target_time = time.time()
        elif c == "right":
            self.target_offset_x -= self.scale / 10
            self.target_time = time.time()

    def update(self, msg):
        self.msg = msg

    def draw(self):
        if not self.msg:
            return

        t = time.time()

        # capture changes in terminal shape at least every 0.25s
        if t - self.last_update_shape_time > 0.25:
            self.canvas.update_shape()
            self.last_update_shape_time = t

        # animation over 0.5s when zooming in/out
        if self.scale != self.target_scale \
                or self.offset_x != self.target_offset_x \
                or self.offset_y != self.target_offset_y:
            animation_fraction = (time.time() - self.target_time) / 0.5
            if animation_fraction > 1.0:
                self.scale = self.target_scale
                self.offset_x = self.target_offset_x
                self.offset_y = self.target_offset_y
            else:
                self.scale = (1 - animation_fraction) * self.scale + animation_fraction * self.target_scale
                self.offset_x = (1 - animation_fraction) * self.offset_x + animation_fraction * self.target_offset_x
                self.offset_y = (1 - animation_fraction) * self.offset_y + animation_fraction * self.target_offset_y

        self.canvas.clear()
        self.canvas.set_color(termgraphics.COLOR_WHITE)

        w = self.canvas.shape[0]
        h = self.canvas.shape[1]

        xmax = self.scale
        ymax = self.scale * h/w

        for command_type, color, data in self.msg_decoder(self.msg):
            if command_type == Space2DViewer.COMMAND_TYPE_POINTS:
                self.canvas.set_color(color)
                x = data[:,0]
                y = data[:,1]

                screen_is = (w * (x - self.offset_x + xmax) / (2 * xmax)).astype(np.uint16)
                screen_js = (h * (1 - (y - self.offset_y + ymax) / (2 * ymax))).astype(np.uint16)

                where_valid = ~np.isnan(screen_is) & ~np.isnan(screen_js) & \
                        (screen_is > 0) & (screen_js > 0) & \
                        (screen_is < w) & (screen_js < h)
                screen_is = screen_is[where_valid]
                screen_js = screen_js[where_valid]

                screen_points = np.vstack((screen_is, screen_js)).T

                self.canvas.points(screen_points)

            elif command_type == Space2DViewer.COMMAND_TYPE_LINE:
                self.canvas.set_color(color)
                screen_0_i = int(w * (data[0][0] - self.offset_x + xmax) / (2 * xmax))
                screen_0_j = int(h * (1 - (data[0][1] - self.offset_y + ymax) / (2 * ymax)))
                screen_1_i = int(w * (data[1][0] - self.offset_x + xmax) / (2 * xmax))
                screen_1_j = int(h * (1 - (data[1][1] - self.offset_y + ymax) / (2 * ymax)))
                self.canvas.line((screen_0_i, screen_0_j), (screen_1_i, screen_1_j))


        self.canvas.set_color((0, 127, 255))
        self.canvas.text(self.title, (0, self.canvas.shape[1] - 4))

        self.canvas.set_color((127, 127, 127))
        self.canvas.text("up/down/left/right: pan   +/-: zoom", (int(self.canvas.shape[0]/3), self.canvas.shape[1] - 4))
        self.canvas.draw()


Space2DViewer.COMMAND_TYPE_POINTS = 0
Space2DViewer.COMMAND_TYPE_LINE = 1
