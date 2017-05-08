#!/usr/bin/env python3

import math
import os
import sys
import time

MODE_BRAILLE = 0
MODE_EASCII = 2

TABLE_EASCII = " '-'.*.|'~/~/F//-\\-~/>-&'\"\"\"/)//.\\\\\\_LLL'\"<C-=CC:\\-\\vD=D|Y|Y|)AH.!i!.ii|/\"/F/Fff//rkfPrkJJ/P/P/P//>brr>kl>&&*=fF/)vb/PPDJ)19/2/R.\\\\\\\\\\\\(=T([(((C=3-5cSct!919|7Ce,\\\\\\_\\\\\\i919i9(C|)\\\\+tv\\|719|7@9_L=L_LLL_=6[CEC[=;==c2ctJ]d=¿Z6E/\\;bsbsbj]SSd=66jj]bddsbJ]j]d]d8"

class TermGraphics(object):
    def __init__(self, mode = MODE_BRAILLE):
        """
        Initialization. This class takes no arguments.
        """
        self.term_shape = list(reversed(list(map(lambda x: int(x), os.popen('stty size', 'r').read().split()))))
        self.shape = (self.term_shape[0]*2, self.term_shape[1]*4)
        self.buffer = bytearray(self.term_shape[0]*self.term_shape[1])
        self.mode = mode
        self.unicode_braille_map = [ \
          0b00000001,
          0b00001000,
          0b00000010,
          0b00010000,
          0b00000100,
          0b00100000,
          0b01000000,
          0b10000000,
        ]

    def clear(self):
        """
        Clear the graphics buffer.
        """
        self.buffer = bytearray(self.term_shape[0]*self.term_shape[1])

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
        if point[0] >= 0 and point[1] >= 0 and point[0] < self.shape[0] and point[1] < self.shape[1]:
            index = ((point[0] >> 1) + (point[1] >> 2) * self.term_shape[0])
            self.buffer[index] = self.buffer[index] | \
              self.unicode_braille_map[(point[0] & 0b1) | ((point[1] & 0b11) << 1)]

    def line(self, point0, point1):
        print("Not yet supported")
        return

    def draw(self):
        """
        Shows the graphics buffer on the screen. Must be called in order to see output.
        """
        sys.stdout.write("\033[H")

        for j in range(self.term_shape[1]):
            sys.stdout.write("\033[" + str(j+1) + ";1H")
            for i in range(self.term_shape[0]):
                if self.mode == MODE_BRAILLE:
                    sys.stdout.write(chr(0x2800 + self.buffer[i + j*self.term_shape[0]]))
                elif self.mode == MODE_EASCII:
                    sys.stdout.write(TABLE_EASCII[self.buffer[i + j*self.term_shape[0]]])
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
