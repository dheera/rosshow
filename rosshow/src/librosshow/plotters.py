import numpy as np

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
          (int(1 + self.left + (self.right - self.left)/2 - (self.right - self.left)/2*math.cos(self.angle)),
          int(1 + self.top + (self.bottom - self.top)/2 + (self.bottom - self.top)/2*math.sin(self.angle))),
          (int(1 + self.left + (self.right - self.left)/2 + (self.right - self.left)/2*math.cos(self.angle)),
          int(1 + self.top + (self.bottom - self.top)/2 - (self.bottom - self.top)/2*math.sin(self.angle))),
        )

class ScopePlotter(object):
    def __init__(self, g, left = 0, right = 1, top = 0, bottom = 1, ymin = -1, ymax = 1, n = 128):
        self.g = g
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.ymax = ymax
        self.ymin = ymin
        self.data = np.array([ 1. ] * n)
        self.pointer = 0

    def get_nice_scale_bound(self, value):
        absvalue = np.abs(value)
        abslogscale = np.ceil(np.log(absvalue) / np.log(10) * 3)
        if abslogscale % 3 == 0:
            return np.sign(value) * (10 ** (abslogscale / 3))
        if abslogscale % 3 == 1:
            return np.sign(value) * (20 ** ((abslogscale - 1) / 3))
        if abslogscale % 3 == 2:
            return np.sign(value) * (50 ** ((abslogscale - 2) / 3))

    def update(self, value):
        self.data[self.pointer] = value
        self.pointer = (self.pointer + 1) % len(self.data)

    def plot(self):
        points = []

        ymin = self.ymin
        ymax = self.ymax

        if ymin is None or ymax is None:
            # Autoscale
            ymax = self.get_nice_scale_bound(np.max(self.data))

            if np.min(self.data) < 0:
                ymin = -ymax
            else:
                ymin = 0.0

        for i in range(len(self.data)):
           points.append(
             (i/len(self.data)*(self.right - self.left) + self.left,
             (1 - (self.data[i] - ymin) / (ymax - ymin)) * (self.bottom - self.top) + self.top)
           )
        self.g.points(points)
        self.g.text("{:2.4f}".format(ymax), (int(self.left), int(self.top)))
        self.g.text("{:2.4f}".format((ymax + ymin)/2), (int(self.left), int(self.top + (self.bottom - self.top) / 2 )))
        self.g.text("{:2.4f}".format(ymin), (int(self.left), int(self.bottom)))

