#!/usr/bin/env python3

import numpy as np
import sensor_msgs.point_cloud2 as pcl2
import librosshow.termgraphics as termgraphics

class PointCloud2Viewer(object):
    def __init__(self):
        self.g = termgraphics.TermGraphics()
        self.scale = 20
        self.altitude = 0.0
        self.azimuth = 0.0
        self.rot_matrix = np.identity(3)
        self.msg = None

    def keypress(self, c):
        if c == "[":
            self.scale *= 1.5
        elif c == "]":
            self.scale /= 1.5
        elif c == "0":
            self.altitude -= 0.1
        elif c == "1":
            self.altitude += 0.1
        elif c == "2":
            self.azimuth -= 0.1
        elif c == "3":
            self.azimuth += 0.1

        self.rot_altitude = \
          np.array([[np.cos(self.azimuth), -np.sin(self.azimuth), 0],
                    [np.sin(self.azimuth), np.cos(self.azimuth), 0],
                    [0, 0, 1]], dtype = np.float32)
        self.rot_azimuth = \
          np.array([[np.cos(self.azimuth), 0, -np.sin(self.azimuth)],
                    [0, 1, 0],
                    [np.sin(self.azimuth), 0, np.cos(self.azimuth)]], dtype = np.float32)

        self.rot_matrix = np.matmul(self.rot_azimuth, self.rot_altitude)

    def update(self, msg):
        self.msg = msg

    def draw(self):
        if not self.msg:
            return

        points = np.array(list(pcl2.read_points(self.msg, skip_nans = True, field_names = ("x", "y", "z"))), dtype = np.float32)
        self.g.clear()
        w = self.g.shape[0]
        h = self.g.shape[1]
        xmax = self.scale
        ymax = xmax * h/w
        rot_points = np.matmul(self.rot_matrix, points.T).T
        for i in range(rot_points.shape[0]):
            q = rot_points[i, :]
            i = int(w * (q[0] + self.scale) / (2 * self.scale))
            j = int(h * (1 - (q[1] + self.scale) / (2 * self.scale)))
            self.g.point((i,j))
        self.g.draw()
