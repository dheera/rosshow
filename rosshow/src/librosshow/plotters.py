import numpy as np
import librosshow.termgraphics as termgraphics
class AnglePlotter(object):
    def __init__(self, g, left = 0, right = 1, top = 0, bottom = 1):
        self.g = g
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.angle = 0

    def update(self, angle):
        self.angle = angle

    def plot(self):
        width, height = self.g.shape
        self.g.rect(
          (int(self.left), int(self.top)),
          (int(self.right), int(self.bottom)),
        )
        self.g.line(
          (int(1 + self.left + (self.right - self.left)/2.0 - (self.right - self.left)/2.0*math.cos(self.angle)),
          int(1 + self.top + (self.bottom - self.top)/2.0 + (self.bottom - self.top)/2.0*math.sin(self.angle))),
          (int(1 + self.left + (self.right - self.left)/2.0 + (self.right - self.left)/2.0*math.cos(self.angle)),
          int(1 + self.top + (self.bottom - self.top)/2.0 - (self.bottom - self.top)/2.0*math.sin(self.angle))),
        )

class ScopePlotter(object):
    def __init__(self, g, left = 0, right = 1, top = 0, bottom = 1, ymin = None, ymax = None, n = 128, title = None):
        self.g = g
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.ymax = ymax
        self.ymin = ymin
        self.data = np.array([ np.nan ] * n, dtype = np.float32)
        self.data[0] = 0.0
        self.pointer = 0
        self.title = title

    def get_nice_scale_bound(self, value):
        if value < 1e-6:
            return 1.0
        absvalue = np.abs(value)
        abslogscale = np.ceil(np.log(absvalue) / np.log(10) * 3)
        if abslogscale % 3 == 0:
            return np.sign(value) * (1 * 10 ** (abslogscale / 3))
        if abslogscale % 3 == 1:
            return np.sign(value) * (2 * 10 ** ((abslogscale - 1) / 3))
        if abslogscale % 3 == 2:
            return np.sign(value) * (5 * 10 ** ((abslogscale - 2) / 3))

    def update(self, value):
        self.data[self.pointer] = value
        self.pointer = (self.pointer + 1) % len(self.data)

    def plot(self):
        points = []

        ymin = self.ymin
        ymax = self.ymax

        if ymin is None or ymax is None:
            # Autoscale
            ymax = self.get_nice_scale_bound(np.nanmax(self.data))

            if np.nanmin(self.data) < 0:
                ymin = -ymax
            else:
                ymin = 0.0

        for i in range(len(self.data)):
           if not np.isnan(self.data[i]):
               points.append(
                 (int(float(i)/len(self.data)*(self.right - self.left) + self.left),
                 int((1.0 - (self.data[i] - ymin) / (ymax - ymin)) * (self.bottom - self.top) + self.top))
               )
            
        self.g.set_color(termgraphics.COLOR_WHITE)
        for i in range(len(points) - 1):
            self.g.line(points[i], points[i+1])

        if self.title:
            self.g.set_color((127, 127, 127))
            self.g.text(self.title, (int((self.left + self.right) / 2 - 2 * len(self.title) / 2), int(self.top)))

        self.g.set_color((63, 63, 63))
        self.g.text("{:2.4f}".format(ymax).rstrip("0").rstrip("."), (int(self.left), int(self.top)))
        self.g.text("{:2.4f}".format((ymax + ymin)/2).rstrip("0").rstrip("."), (int(self.left), int(self.top + (self.bottom - self.top) / 2 )))
        self.g.text("{:2.4f}".format(ymin).rstrip("0").rstrip("."), (int(self.left), int(self.bottom)))

