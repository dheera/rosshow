import numpy as np
import time

import librosshow.termgraphics as termgraphics

class LaserScanViewer(object):
    def __init__(self, canvas, title = ""):
        self.g = canvas
        self.scale = 10.0
        self.target_scale = 10.0
        self.target_scale_time = 0
        self.msg = None
        self.last_update_shape_time = 0
        self.title = title

    def keypress(self, c):
        if c == "+" or c == "=":
            self.target_scale /= 1.5
            self.target_scale_time = time.time()
        elif c == "-":
            self.target_scale += 1.5
            self.target_scale_time = time.time()

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

        # animation over 0.5s when zooming in/out
        if self.scale != self.target_scale:
            animation_fraction = (time.time() - self.target_scale_time) / 0.5
            if animation_fraction > 1.0:
                self.scale = self.target_scale
            else:
                self.scale = (1 - animation_fraction) * self.scale + animation_fraction * self.target_scale

        self.g.clear()
        self.g.set_color(termgraphics.COLOR_WHITE)

        w = self.g.shape[0]
        h = self.g.shape[1]

        xmax = self.scale
        ymax = self.scale * h/w

        angles = np.linspace(self.msg.angle_min, self.msg.angle_max, len(self.msg.ranges), dtype = np.float32)
        ranges = np.array(self.msg.ranges, dtype = np.float32)
        x = ranges * np.cos(angles)
        y = ranges * np.sin(angles)
        screen_is = (w * (x + xmax) / (2 * xmax)).astype(np.uint16)
        screen_js = (h * (1 - (y + ymax) / (2 * ymax))).astype(np.uint16)

        where_valid = ~np.isnan(angles) & ~np.isnan(ranges) & \
                (screen_is > 0) & (screen_js > 0) & \
                (screen_is < w) & (screen_js < h)
        screen_is = screen_is[where_valid]
        screen_js = screen_js[where_valid]

        points = np.vstack((screen_is, screen_js)).T
        self.g.points(points)

        self.g.set_color((0, 127, 255))
        self.g.text(self.title, (0, self.g.shape[1] - 4))

        self.g.set_color((127, 127, 127))
        self.g.text("+/-: zoom", (int(self.g.shape[0]/3), self.g.shape[1] - 4))
        self.g.draw()


