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


class Signal:

    def __init__(self):
        self.callbacks = None

    def connect(self, callback, extra_arg=None):
        if self.callbacks is None:
            self.callbacks = []
        self.callbacks.append((callback, extra_arg))

    def emit(self, *params):
        if self.callbacks is None:
            return
        for cb, extra_arg in self.callbacks:
            if extra_arg:
                cb(extra_arg, *params)
            else:
                cb(*params)
