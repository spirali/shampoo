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


from base.events import Signal


class ProjectPart:

    def __init__(self, parent):
        self.parent = parent
        self.on_update = Signal()

    @property
    def project(self):
        return self.parent.project

    def update(self):
        self.on_update.emit()


class Project:

    def __init__(self):
        pass

    @property
    def project(self):
        return self
