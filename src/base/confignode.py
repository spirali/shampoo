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


import PyQt4.QtCore as QtCore
import base.colortable

from base.renderitem import RenderItem
from enum import Enum


class SceneState(Enum):

    NoScene = 1
    HasScene = 2
    HasSceneExclusive = 3


class ConfigNode:

    def __init__(self, name=None,
                 owner=None,
                 mesh_object=False,
                 scene=False,
                 scene_exclusive=False,
                 visible=None):
        self.childs = []
        self.parent = None
        self._name = name
        self.owner = owner
        self.color = None
        self.editor = None
        self.has_mesh_object = mesh_object

        if scene_exclusive:
            self.scene_state = SceneState.HasSceneExclusive
            self.visible = True
        elif scene or mesh_object:
            self.scene_state = SceneState.HasScene
            self.visible = True
        else:
            self.scene_state = SceneState.NoScene
            self.visible = False

        if visible is not None:
            self.visible = visible

        if name is None and owner:
            owner.on_update.connect(self.update)

    @property
    def name(self):
        if self._name is None and self.owner:
            return self.owner.name
        else:
            return self._name

    def get_tree(self):
        return self.parent.get_tree()

    def index_of_child(self, child):
        return self.childs.index(child)

    def collect_render_items(self, items):
        if not self.visible:
            return
        for node in self.childs:
            node.collect_render_items(items)
        if self.has_mesh_object:
            render_item = RenderItem(self.owner.make_mesh_object(), self.color)
            items.append(render_item)

    def collect_subnodes(self, nodes):
        nodes.append(self)
        for node in self.childs:
            node.collect_subnodes(nodes)

    def get_subnodes(self):
        nodes = []
        self.collect_subnodes(nodes)
        return nodes

    def set_colors(self):
        nodes = (node for node in self.get_subnodes() if node.has_mesh_object)
        for node, color in zip(nodes,
                               base.colortable.colors_gen()):
            node.color = color

    def add_node(self, node):
        node.parent = self
        self.childs.append(node)

    def get_data(self, role):
        if role == QtCore.Qt.DisplayRole:
            return self.name
        elif role == QtCore.Qt.DecorationRole:
            return self.color
        elif role == QtCore.Qt.CheckStateRole:
            if self.scene_state is not SceneState.NoScene:
                if self.visible:
                    return QtCore.Qt.Checked
                else:
                    return QtCore.Qt.Unchecked

    def set_data(self, role, value):
        if role == QtCore.Qt.CheckStateRole:
            self.visible = value == QtCore.Qt.Checked
            if self.scene_state == SceneState.HasSceneExclusive:
                for child in self.parent.childs:
                    if child.visible and child is not self:
                        child.visible = False
                        child.update()
            self.get_tree().rebuild_scene.emit()
        return True

    def get_flags(self, default):
        if self.scene_state is not SceneState.NoScene:
            return default | QtCore.Qt.ItemIsUserCheckable
        else:
            return default

    def make_editor(self, layout):
        if self.editor:
            self.editor.build(self.owner, layout)

    def update(self):
        tree = self.get_tree()
        if tree:
            tree.notify_node_changed(self)

    def __repr__(self):
        return "<ConfigNode name={0._name}>".format(self)
