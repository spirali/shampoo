#
#    Copyright (C) 2014 Stanislav Bohm
#
#    This file is part of Shampoo.
#
#    Shampoo is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    Shampoo is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Shampoo.  If not, see <http://www.gnu.org/licenses/>.
#


import math


def vec_length(v):
    x, y, z = v
    return math.sqrt(x * x + y * y + z * z)

def vec_normalize(v):
    l = vec_length(v)
    if l == 0:
        return (0.0, 0.0, 0.0)
    return (v[0] / l, v[1] / l, v[2] / l)

def vec_make(v1, v2):
    return (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v2[2])

def vec_diff(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])

def vec_midpoint(v1, v2):
    return ((v1[0] + v2[0]) / 2, (v1[1] + v2[1]) / 2, (v1[2] + v2[2]) / 2)

def vec_neg(v):
    return (-v[0], -v[1], -v[2])


class BoundingBox:

    def __init__(self):
        self.reset()

    @property
    def size(self):
        return vec_diff(self.max_point, self.min_point)

    @property
    def center(self):
        return vec_midpoint(self.max_point, self.min_point)

    @property
    def diameter(self):
        return max(*self.size)

    def reset(self):
        self.min_point = None
        self.max_point = None

    def is_valid(self):
        return self.min_point is not None

    def add_points(self, points):
        for point in points:
            self.add_point(point)

    def add_point(self, point):
        if self.min_point is None:
            self.min_point = point
            self.max_point = point
        else:
            self.min_point = (min(self.min_point[0], point[0]),
                              min(self.min_point[1], point[1]),
                              min(self.min_point[2], point[2]))
            self.max_point = (max(self.max_point[0], point[0]),
                              max(self.max_point[1], point[1]),
                              max(self.max_point[2], point[2]))

    def add_box(self, bbox):
        if bbox.is_valid():
            self.add_point(bbox.min_point)
            self.add_point(bbox.max_point)

    def merge(self, bbox):
        b = BoundingBox()
        b.add_box(self)
        b.add_box(bbox)
        return b
