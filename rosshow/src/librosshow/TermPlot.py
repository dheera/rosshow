#!/usr/bin/env python3

import math
import os
import numpy
import sys
import time

class TermGraphics(object):

    def __init__(self):
        self.terminal_size = self._get_terminal_size()

    # private

    def _get_terminal_size():
        return list(map(lambda x: int(x), os.popen('stty size', 'r').read().split()))

    # public

    def points(self, points):
        for point in points:
            self.point(point)

    def point(self, point):

    def line(self, point0, point1):

    def draw(self):

def mat2braille(points):
    matrix_width, matrix_height = points.shape
    braille = numpy.zeros((int(matrix_width/2), int(matrix_height/4)), dtype = numpy.int32)
    for i in range(int(matrix_width/2)):
        for j in range(int(matrix_height/4)):
             subset = list(map(lambda x:int(x), list(points[2*i:2*i+2, 4*j:4*j+4].reshape(8,1))))
             braille[i,j] = 0x2800 + (\
               subset[0] | \
               subset[4]<<3 | \
               subset[1]<<1 | \
               subset[5]<<4 | \
               subset[2]<<2 | \
               subset[6]<<5 | \
               subset[3]<<6 | \
               subset[7]<<7 \
             )
    return braille

def on_pc2(pc2):
    global xmin, xmax, ymin, ymax
    points = list(pcl2.read_points(pc2))

    screen_height, screen_width = get_terminal_size() 

    matrix_height = 4 * screen_height
    matrix_width = 2 * screen_width

    matrix = numpy.zeros((matrix_width, matrix_height))

    for x, y, z in points:
        i = int(matrix_width * (x - xmin) / (xmax - xmin))
        j = int(matrix_height * (y - ymin) / (ymax - ymin))
        if i >= 0 and i < matrix_width and j >= 0 and j < matrix_height:
            matrix[i, j] = 1

    screen = mat2braille(matrix)

    sys.stdout.write("\r100%\033[H")

    for j in range(screen_height):
        for i in range(screen_width):
            sys.stdout.write(chr(screen[i,j]))
    sys.stdout.flush()

if __name__ == '__main__':

    if len(sys.argv) > 1:
        TOPIC = sys.argv[1]
    else:
        TOPIC = "/pc2"

    screen_height, screen_width = get_terminal_size()

    xmax = 20
    xmin = -20
    ymax = screen_height/screen_width * (xmax - xmin)
    ymin = -ymax

    rospy.init_node('rosstorm_' + str(int(time.time())))
    rospy.Subscriber(TOPIC, PointCloud2, on_pc2)

    rospy.spin()
