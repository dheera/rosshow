#!/usr/bin/env python3

import math
import os
import numpy
import sys
import time

class TermGraphics(object):
    def __init__(self):
        """
        Initialization. This class takes no arguments.
        """
        self.shape = list(reversed(list(map(lambda x: int(x), os.popen('stty size', 'r').read().split()))))
        self.buffer = numpy.zeros((self.shape[0]*2, self.shape[1]*4), dtype = numpy.uint8)
        self.screen_buffer = numpy.zeros(self.shape, dtype = numpy.uint8)

    def clear(self):
        """
        Clear the graphics buffer.
        """
        self.buffer = numpy.zeros((self.shape[0]*2, self.shape[1]*4), dtype = numpy.uint8)

    def points(self, points):
        """
        Draws a list of points = [(x0,y0), (x1,y1), (x2,y2), ...].
        """
        for point in points:
            self.point(point)

    def point(self, point):
        """
        Draw a point at points = (x,y) where x is the column number, y is the row number, and (0,0)
        is the top-left corner of the screen.
        """
        if point[0] >= 0 and point[1] >= 0 and point[0] < 2*self.shape[0] and point[1] < 4*self.shape[1]:
            self.buffer[point] = 1

    def line(self, point0, point1):
        print("Not yet supported")
        return

    def draw(self):
        """
        Shows the graphics buffer on the screen. Must be called in order to see output.
        """
        for i in range(int(self.shape[0])):
             for j in range(int(self.shape[1])):
                 subset = list(map(lambda x:int(x), list(self.buffer[2*i:2*i+2, 4*j:4*j+4].reshape(8,1))))
                 self.screen_buffer[i,j] = (\
                   subset[0] | \
                   subset[4]<<3 | \
                   subset[1]<<1 | \
                   subset[5]<<4 | \
                   subset[2]<<2 | \
                   subset[6]<<5 | \
                   subset[3]<<6 | \
                   subset[7]<<7 \
                 )

        sys.stdout.write("\033[H")

        for j in range(self.shape[1]):
            sys.stdout.write("\033[" + str(j+1) + ";1H")
            for i in range(self.shape[0]):
                sys.stdout.write(chr(0x2800 + self.screen_buffer[i,j]))
        sys.stdout.flush()


if __name__ == '__main__':
    # perform a test if run directly
    g = TermGraphics()
    for j in range(10):
        g.clear()
        for i in range(300):
            g.point((i, int(i*j/5)))
        g.draw()
        time.sleep(0.1)
