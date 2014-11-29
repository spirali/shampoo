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


from base.geom import vec_normalize, BoundingBox


class MeshObject:

    def __init__(self):
        self.vertices = []
        self.normals = None
        self.bounding_box = None

    def add_triangle(self, p1, p2, p3):
        self.vertices.append(p1)
        self.vertices.append(p2)
        self.vertices.append(p3)

    def add_quad(self, p1, p2, p3, p4):
        self.add_triangle(p1, p2, p3)
        self.add_triangle(p3, p4, p1)

    def add_polygon(self, polygon):
        l = len(polygon)
        if l == 3:
            self.add_triangle(*polygon)
        elif l == 4:
            self.add_quad(*polygon)
        else:
            assert l >= 5
            p = polygon[0]
            for i in range(1, l - 1):
                self.add_triangle(p, polygon[i], polygon[i+1])

    def finish(self):

        self.bounding_box = BoundingBox()
        self.bounding_box.add_points(self.vertices)

        self.normals = []

        for i in range(0, len(self.vertices), 3):
            v1x, v1y, v1z = self.vertices[i]
            v2x, v2y, v2z = self.vertices[i + 1]
            v3x, v3y, v3z = self.vertices[i + 2]

            ux = v2x - v1x
            uy = v2y - v1y
            uz = v2z - v1z

            vx = v3x - v1x
            vy = v3y - v1y
            vz = v3z - v1z

            n = vec_normalize((uy * vz - uz * vy,
                               uz * vx - ux * vz,
                               ux * vy - uy * vx))
            self.normals.append(n)
            self.normals.append(n)
            self.normals.append(n)
