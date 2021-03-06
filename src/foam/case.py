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


from base.configtree import ConfigTree
from base.events import Signal
from base.project import Project
from foam.basemesh import BaseMesh
from foam.datatypes import FoamDict
from foam.foamfile import FoamFile
from foam.snapping import Snapping

import logging
import os.path


class Case(Project):

    def __init__(self):
        super().__init__()
        self.path = None
        self.basemesh = BaseMesh(self)
        self.snapping = Snapping(self)
        self.control_dict = self._make_default_control_dict()

        self.need_redraw = Signal()
        self.rebuild_scene = Signal()

    def load(self, path):
        self.path = path
        logging.info("Loading project '%s'", self.path)
        self.basemesh.load()

    def save(self):
        logging.info("Saving project as '%s'", self.path)
        self.basemesh.save()

        ff = FoamFile(self.get_filename("system", "controlDict"))
        ff.set_header_dict("dictionary", "controlDict")
        ff.write_dictionary(self.control_dict)


    def get_filename(self, *args):
        return os.path.join(*((self.path,) + args))

    def make_tree(self, parent=None):
        tree = ConfigTree(parent)
        tree.add_node(self.basemesh.make_cnode())
        tree.add_node(self.snapping.make_cnode())
        tree.set_colors()
        return tree

    def _make_default_control_dict(self):
        fd = FoamDict()
        fd.add("startFrom", "startTime")
        fd.add("startTime", 0.0)
        fd.add("stopAt", "endTime")
        fd.add("endTime", 1000.0)
        fd.add("deltaT", 1.0)
        fd.add("writeControl", "timeStep")
        fd.add("writeInterval", 1000.0)
        fd.add("purgeWrite", 0)
        fd.add("writeFormat", "ascii")
        fd.add("writeCompression", "uncompressed")
        fd.add("timeFormat", "general")
        fd.add("timePrecision", 6)
        fd.add("graphFormat", "raw")
        fd.add("runTimeModifiable", "yes")
        return fd
