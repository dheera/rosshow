#!/usr/bin/env python3

import sensor_msgs.point_cloud2 as pcl2

from .termgraphics import TermGraphics

class PointCloud2Viewer(object):
    def __init__(self):
        self.g = TermGraphics()
        self.xmax = 20
        self.ymax = 20

    def update(self, data):
        points = list(pcl2.read_points(data))
        self.g.clear()
        w = self.g.shape[0]
        h = self.g.shape[1]
        self.ymax = self.xmax * h/w
        for x, y, z in points:
            i = int(w * (x + self.xmax) / (2 * self.xmax))
            j = int(h * (1 - (y + self.ymax) / (2 * self.ymax)))
            self.g.point((i,j))
        self.g.draw()
