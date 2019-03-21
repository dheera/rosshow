#!/usr/bin/env python3

import math

import librosshow.termgraphics as termgraphics

class LaserScanViewer(object):
    def __init__(self):
        self.g = termgraphics.TermGraphics()
        self.xmax = 10
        self.ymax = 10
        self.msg = None

    def update(self, msg):
        self.msg = msg

    def draw(self):
        if not self.msg:
            return

        self.g.clear()
        w = self.g.shape[0]
        h = self.g.shape[1]
        self.ymax = self.xmax * h/w
        for n in range(len(self.msg.ranges)):
            if math.isinf(self.msg.ranges[n]) or math.isnan(self.msg.ranges[n]):
                continue
            x = self.msg.ranges[n]*math.cos(self.msg.angle_min + n*self.msg.angle_increment)
            y = self.msg.ranges[n]*math.sin(self.msg.angle_min + n*self.msg.angle_increment)
            i = int(w * (x + self.xmax) / (2 * self.xmax))
            j = int(h * (1 - (y + self.ymax) / (2 * self.ymax)))
            self.g.point((i, j))

        self.g.draw()
