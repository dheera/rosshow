#!/usr/bin/env python3

import math

from .termgraphics import TermGraphics

class LaserScanViewer(object):
    def __init__(self):
        self.g = TermGraphics()
        self.xmax = 10
        self.ymax = 10

    def update(self, data):
        self.g.clear()
        w = self.g.shape[0]
        h = self.g.shape[1]
        self.ymax = self.xmax * h/w
        for n in range(len(data.ranges)):
            if data.ranges[n] == math.inf:
                continue
            x = data.ranges[n]*math.cos(data.angle_min + n*data.angle_increment)
            y = data.ranges[n]*math.sin(data.angle_min + n*data.angle_increment)
            i = int(w * (x + self.xmax) / (2 * self.xmax))
            j = int(h * (1 - (y + self.ymax) / (2 * self.ymax)))
            self.g.point((i,j))
        self.g.draw()
