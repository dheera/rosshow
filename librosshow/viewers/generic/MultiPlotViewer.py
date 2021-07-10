import time
import math
import librosshow.termgraphics as termgraphics
from librosshow.plotters import ScopePlotter, AnglePlotter
import operator


class MultiPlotViewer(object):
    def __init__(self, canvas, title = "", data_fields=[], columns=3):
        self.g = canvas
        self.last_update_shape_time = 0
        self.title = title
        self.right = 10
        self.data_fields = data_fields
        self.last_values = [0] *len(data_fields)

        hmargin = self.g.shape[0]/40.
        vmargin = self.g.shape[1]/20.
        hsize = (self.g.shape[0] - 4*hmargin ) / (columns)
        vsize = (self.g.shape[1] - 4*vmargin ) / (math.floor(len(data_fields)/columns))

        self.data_scope_plotters = []
        row = 0 
        column = 0
        for data in data_fields:
            self.data_scope_plotters.append(ScopePlotter(self.g,
                left = hmargin + (hmargin + hsize) * column,
                top = vmargin + (vmargin + vsize) * row,
                right = hmargin + (column+1) * (hsize),
                bottom = vmargin + (row+1) * (vsize),
                ymin = None,
                ymax = None,
                title = data,
            ))
            column = column + 1
            if (column == columns):
                row = row + 1
                column = 0
            

    def keypress(self, c):
        return

    def update(self, msg):
        for i in range(len(self.data_fields)):
            self.last_values[i] = float(operator.attrgetter(self.data_fields[i])(msg))
            self.data_scope_plotters[i].update(self.last_values[i])

    def draw(self):
        t = time.time()

        # capture changes in terminal shape at least every 0.5s
        if t - self.last_update_shape_time > 0.25:
            self.g.update_shape()
            self.last_update_shape_time = t

        self.g.clear()
        for data_scope_plotter in self.data_scope_plotters:
            data_scope_plotter.plot()
        if self.title:
            self.g.set_color((0, 127, 255))
            self.g.text(self.title, (0, self.g.shape[1] - 4))
        self.g.draw()
