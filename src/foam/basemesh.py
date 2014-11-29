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
from base.meshobj import MeshObject
from base.project import ProjectPart
from foam.datatypes import FoamArray, FoamDict
from foam.foamfile import FoamFile
from ui.editor import EditorBuilder

from itertools import chain


def make_cnode_for_list(name, lst, **kw):
    cnode = ConfigNode(name, **kw)
    for obj in lst:
        cnode.add_node(obj.make_cnode())
    return cnode


class BaseMesh(ProjectPart):

    config_attrs = ("convert_to_meters",)

    def __init__(self, parent):
        super().__init__(parent)
        self.convert_to_meters = 1.0
        self.blocks = [ MeshBlock(self) ]

        # Default box vertices
        self.vertices = [
                    (-1.0, -1.0, -1.0),
                    (1.0, -1.0, -1.0),
                    (1.0, -1.0, 1.0),
                    (-1.0, -1.0, 1.0),
                    (-1.0, 1.0, -1.0),
                    (1.0, 1.0, -1.0),
                    (1.0, 1.0, 1.0),
                    (-1.0, 1.0, 1.0) ]
        self.boundaries = self.blocks[0].make_basic_boundaries()

    def make_cnode(self):
        cnode = ConfigNode("Base mesh", self, scene=True)
        cnode.editor = EditorBuilder()
        group = cnode.editor.add_group("Basic configurations")
        group.add_float("ConvertToMeters", "convert_to_meters")
        n = make_cnode_for_list(
                "Blocks", self.blocks, scene_exclusive=True)
        cnode.add_node(n)
        n = make_cnode_for_list(
                "Boundaries", self.boundaries,
                scene_exclusive=True, visible=False)
        cnode.add_node(n)
        return cnode

    def get_foam_file(self):
        return FoamFile(self.project.get_filename(
                "constant", "polyMesh", "blockMeshDict"))

    def save(self):
        d = FoamDict()
        d.add("convertToMeters", self.convert_to_meters),
        d.add("vertices", FoamArray(self.vertices, recursive=True))
        d.add("edges", FoamArray())
        d.add("blocks", FoamArray(chain.from_iterable(
                                     b.get_save_item() for b in self.blocks)))
        d.add("boundary", FoamArray(b.get_save_item() for b in self.boundaries))
        ff = self.get_foam_file()
        ff.set_header_dict("dictionary", "blockMeshDict")
        ff.write_dictionary(d)

    def load(self):
        ff = self.get_foam_file()
        ff.read_as_dictionary()
        content = ff.content
        self.convert_to_meters = content.get_float("convertToMeters")
        self.vertices= content.get("vertices").clean_list()
        blocks = content.get("blocks").items
        self.blocks = [ MeshBlock(self,
                                  ff,
                                  blocks[i:i + 3])
                        for i in range(0, len(blocks), 3) ]
        self.boundaries = [ MeshBoundary(self, ff=ff, ff_boundary=ff_boundary)
                            for ff_boundary in content.get("boundary") ]


class MeshBlock(ProjectPart):

    config_attrs = ("cellsX", "cellsY", "cellsZ")

    def __init__(self, parent, ff=None, ff_block=None):
        super().__init__(parent)

        if ff is not None:
            indices, cells, grading = ff_block
            assert indices.name == "hex"
            self.indices = indices.clean_list()
            assert len(self.indices) == 8
            self.cells_x, self.cells_y, self.cells_z = cells
        else:
            self.cells_x = 16
            self.cells_y = 16
            self.cells_z = 16
            self.indices = list(range(8))

    def make_basic_boundaries(self):
        return [
            MeshBoundary(self, name="block_x1", faces=[(0, 4, 7, 3)]),
            MeshBoundary(self, name="block_x2", faces=[(1, 2, 6, 5)]),
            MeshBoundary(self, name="block_y1", faces=[(0, 1, 5, 4)]),
            MeshBoundary(self, name="block_x2", faces=[(3, 7, 6, 2)]),
            MeshBoundary(self, name="block_z1", faces=[(0, 3, 2, 1)]),
            MeshBoundary(self, name="block_z2", faces=[(4, 5, 6, 7)]),
        ]

    def make_cnode(self):
        cnode = ConfigNode("Block", owner=self, mesh_object=True)
        cnode.editor = self.editor
        return cnode

    @property
    def vertices(self):
        return [ self.parent.vertices[i] for i in self.indices ]

    def make_mesh_object(self):
        p = self.vertices
        mesh_object = MeshObject()
        mesh_object.add_quad(p[0], p[4], p[7], p[3])
        mesh_object.add_quad(p[1], p[2], p[6], p[5])
        mesh_object.add_quad(p[0], p[1], p[5], p[4])
        mesh_object.add_quad(p[3], p[7], p[6], p[2])
        mesh_object.add_quad(p[0], p[3], p[2], p[1])
        mesh_object.add_quad(p[4], p[5], p[6], p[7])
        mesh_object.finish()
        return mesh_object

    def update_vertices(self):
        self.project.rebuild_scene.emit()

    def get_vertex(self, i):
        return self.parent.vertices[self.indices[i]]

    def set_vertex(self, i, value):
        self.parent.vertices[self.indices[i]] = value
        self.update_vertices()

    def get_save_item(self):
        return [ FoamArray(self.indices, "hex"),
                 FoamArray((self.cells_x, self.cells_y, self.cells_z)),
                 FoamArray((1, 1, 1), "simpleGrading") ]

    @classmethod
    def init(cls):
        def get_vertex(i):
            return lambda obj: obj.get_vertex(i)
        def set_vertex(i):
            return lambda obj, value: obj.set_vertex(i, value)
        cls.editor = EditorBuilder()
        group = cls.editor.add_group("Cells")
        group.add_int("Cells X", "cells_x", min_value=1, max_value=1000000000)
        group.add_int("Cells Y", "cells_y", min_value=1, max_value=1000000000)
        group.add_int("Cells Z", "cells_z", min_value=1, max_value=1000000000)

        group = cls.editor.add_group("Vertices")
        for i in range(8):
            group.add_vertex("V{0}".format(i), (get_vertex(i), set_vertex(i)),
                             update_method=None)

MeshBlock.init()


class MeshBoundary(ProjectPart):

    def __init__(self, parent, name=None, faces=None,
                 ff=None, ff_boundary=None):
        super().__init__(parent)
        if ff is not None:
            self.name = ff_boundary.name
            self.type = ff_boundary.get("type")
            self.faces = ff_boundary.get("faces")
        else:
            self.name = name
            self.faces = faces
            self.type = "patch"

    def make_cnode(self):
        cnode = ConfigNode(owner=self, mesh_object=True)
        cnode.editor = self.editor
        return cnode

    def make_mesh_object(self):
        mesh_object = MeshObject()
        for face in self.faces:
            mesh_object.add_polygon(
                    [ self.parent.vertices[i] for i in face ])
        mesh_object.finish()
        return mesh_object

    def get_save_item(self):
        d = FoamDict(self.name)
        d.add("type", self.type)
        d.add("faces", FoamArray(self.faces, recursive=True))
        return d

    @classmethod
    def init(cls):
        cls.editor = EditorBuilder()
        group = cls.editor.add_group("Boundary")
        group.add_string("Name", "name", identifier=True)
        group.add_choose("Type", "type",
                options = (("Patch", "patch"),
                           ("Wall", "wall"),
                           ("Empty", "empty"),
                           ("Symmetry plane", "symmetryPlane")))


MeshBoundary.init()
