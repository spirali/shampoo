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


import base.paths as paths

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMatrix4x4, QVector3D
import OpenGL.GL as GL
import PyQt4.QtOpenGL as QtOpenGL
import logging
import os.path


class GLWidget(QtOpenGL.QGLWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0
        self.zoom = 1.0
        self.center = (0.0, 0.0, 0.0)
        self.scale = 1.0
        self.shaders = None
        self.last_pos = None

        from base.renderitem import RenderItem
        from base.meshobj import MeshObject
        import PyQt4.QtGui
        m = MeshObject()
        m.add_triangle((0, 0, 0), (1, 0, 1), (1, 1, 1))
        self.render_items = [
                RenderItem(m, PyQt4.QtGui.QColor("red"))
        ]

    def initializeGL(self):
        GL.glHint(GL.GL_PERSPECTIVE_CORRECTION_HINT, GL.GL_NICEST)
        self.shaders = [ self.load_shader("basic"),
                         self.load_shader("light") ]

    def paintGL(self):
        self.render(False)

    def resizeGL(self, width, height):
        self.width = width
        self.height = height

    def focus_on_bounding_box(self, bounding_box):
        self.scale = 0.6 / bounding_box.diameter
        self.center = bounding_box.center
        self.zoom = 1.0
        self.update()

    def render(self, pickmode):
        GL.glViewport(0, 0, self.width, self.height)
        GL.glClearDepth(1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)

        GL.glClearColor(0.3, 0.3, 0.3, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        perspective_m = self.create_perspective_matrix()
        camera_m = self.create_camera_matrix(True)
        view_m = perspective_m * camera_m

        program = self.shaders[1]
        program.bind()

        program.enableAttributeArray("qt_Vertex")
        program.enableAttributeArray("qt_Normal")
        program.setUniformValue("qt_ModelViewProjectionMatrix", view_m)
        program.setUniformValue("qt_NormalMatrix", camera_m.normalMatrix())

        program.enableAttributeArray("qt_Vertex")
        for render_item in self.render_items:
            self.draw_item(program, render_item)

        program.release()

    def draw_item(self, program, render_item):
            vertices = render_item.mesh_object.vertices
            normals = render_item.mesh_object.normals
            if not vertices:
                return
            program.setAttributeArray("qt_Vertex", vertices)
            program.setAttributeArray("qt_Normal", normals)
            program.setUniformValue("color", render_item.color)
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(vertices))

    def create_perspective_matrix(self):
        m = QMatrix4x4()
        m.perspective(45.0, float(self.width) / self.height, 0.01, 10000.0)
        return m

    def create_camera_matrix(self, use_center):
        m = QMatrix4x4()
        m.translate(0.0, 0.0, -1.5 * self.zoom)
        m.rotate(self.rot_x, 1.0, 0.0, 0.0)
        m.rotate(self.rot_y, 0.0, 1.0, 0.0)
        m.rotate(self.rot_z, 0.0, 0.0, 1.0)
        if use_center:
            m.scale(QVector3D(self.scale, self.scale, self.scale))
            x, y, z = self.center
            m.translate(-x, -y, -z)
        return m

    def load_shader(self, name):
        logging.debug("Loading shaders %s", name)
        program = QtOpenGL.QGLShaderProgram(self)
        filename = os.path.join(paths.SHADERS, name + ".vert")
        if not program.addShaderFromSourceFile(QtOpenGL.QGLShader.Vertex,
                                               filename):
            raise Exception("Compilation of vertex shader failed")

        filename = os.path.join(paths.SHADERS, name + ".frag")
        if not program.addShaderFromSourceFile(QtOpenGL.QGLShader.Fragment,
                                               filename):
            raise Exception("Compilation of fragment shader failed")
        if not program.link():
            raise Exception("Linking of shaders failed")
        return program

    def rotate(self,x, y, z):
        self.rot_x += x
        self.rot_y += y
        self.rot_z += z
        self.update()

    def mousePressEvent(self, event):
        self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.RightButton and self.last_pos:
            dx = event.x() - self.last_pos.x()
            dy = event.y() - self.last_pos.y()
            self.rotate(dy / 2.0, dx / 2.0, 0)
        self.last_pos = event.pos()

    def wheelEvent(self, event):
        if event.orientation() == Qt.Vertical:
            f = abs(event.delta()) / 120 * 1.4
            if event.delta() > 0:
                self.zoom /= f
            else:
                self.zoom *= f
        self.update()
