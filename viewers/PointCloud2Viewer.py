#!/usr/bin/env python3

import sensor_msgs.point_cloud2 as pcl2

from .TermGraphics import TermGraphics

class PointCloud2Viewer(object):
    def __init__(self):
        self.g = TermGraphics()
        self.xmin = -10
        self.xmax = 10
        self.ymin = -10
        self.ymax = 10

    def update(self, data):
        points = list(pcl2.read_points(data))
        self.g.clear()
        w = self.g.shape[0]*2
        h = self.g.shape[1]*4
        for x, y, z in points:
            i = int(w * (x - self.xmin) / (self.xmax - self.xmin))
            j = int(h * (y - self.ymin) / (self.ymax - self.ymin))
            self.g.point((i,j))
        self.g.draw()
