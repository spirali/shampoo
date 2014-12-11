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


from base.confignode import ConfigNode
from base.project import ProjectPart
from ui.editor import EditorBuilder

class Snapping(ProjectPart):

    def __init__(self, parent):
        super().__init__(parent)
        self.castellated_mesh = True
        self.snap = True
        self.layers = True
        self.merge_tolerance = 1e-06;
        self.debug = 0
        self.geometry = Geometry(self)

    def make_cnode(self):
        cnode = ConfigNode("Snapping", self)
        cnode.editor = self.editor
        cnode.add_node(self.geometry.make_cnode())
        return cnode

    @classmethod
    def init(cls):
        cls.editor = EditorBuilder()
        group = cls.editor.add_group("Basic options")
        group.add_bool("Castellated mesh", "castellated_mesh")
        group.add_bool("Snap", "snap")
        group.add_bool("Layers", "layers")
        group = cls.editor.add_group("Debugging")
        group.add_choose(
                None,
                "debug",
                options=(("No debug - Write final mesh only", 0),
                    ("Debug 1 - Write intermediate meshes", 1),
                    ("Debug 2 - Write volScalarField with cellLevel", 2),
                    ("Debug 4 - Write intersections as .obj files", 4)))


Snapping.init()


class Geometry(ProjectPart):

    def __init__(self, parent):
        super().__init__(parent)

    def make_cnode(self):
        cnode = ConfigNode("Geometry", self, scene=True)
        return cnode
