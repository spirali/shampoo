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
from base.events import Signal

import PyQt4.QtCore as QtCore


class ConfigTree(ConfigNode, QtCore.QAbstractItemModel):

    def __init__(self, parent=None):
        ConfigNode.__init__(self, None, scene=True)
        QtCore.QAbstractItemModel.__init__(self, parent)

        self.rebuild_scene = Signal()

    def set_parent(self, node):
        raise Exception("ConfigTree cannot be used as child")

    def get_tree(self):
        return self

    """
    def test(self):
        n = ConfigNode("Moje noda")
        n.color = QtGui.QColor("red")
        self.add_node(n)
        n = ConfigNode("Druha noda")
        self.add_node(n)
    """

    def columnCount(self, index):
        return 1

    def rowCount(self, index):
        if index.column() > 0:
            return 0

        if index.isValid():
            node = index.internalPointer()
        else:
            node = self

        return len(node.childs)

    def hasChildren(self, index):
        return self.rowCount(index) > 0

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        node = index.internalPointer()
        if node.parent == self:
            return QtCore.QModelIndex()
        row = node.parent.index_of_child(node)
        return self.createIndex(row, 0, node.parent)

    def index(self, row, column, index):
        if not self.hasIndex(row, column, index):
            return QtCore.QModelIndex()

        if index.isValid():
            node = index.internalPointer()
        else:
            node = self
        return self.createIndex(row, column, node.childs[row])

    def data(self, index, role):
        return index.internalPointer().get_data(role)

    def setData(self, index, value, role):
        return index.internalPointer().set_data(role, value)

    def flags(self, index):
        return index.internalPointer().get_flags(super().flags(index))

    def get_index(self, node):
        if node == self:
            return QtCore.QModelIndex()
        return self.createIndex(node.parent.index_of_child(node), 0, node)

    def notify_node_changed(self, node):
        index = self.get_index(node)
        self.dataChanged.emit(index, index)
