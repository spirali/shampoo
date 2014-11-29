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


class Pointer:

    def __init__(self, obj, attr, update_callback):
        self.obj = obj
        self.attr = attr
        self.update_callback = update_callback

    def get(self):
        return self._get(self.obj, self.attr)

    def _get(self, obj, attr):
        if isinstance(attr, str):
            return getattr(obj, attr)
        elif isinstance(attr, int):
            return obj[attr]
        else:
            for a in attr:
                obj = self._get(obj, a)
            return obj

    def set(self, value):
        self._set(self.obj, self.attr, value)
        if self.update_callback:
            self.update_callback()

    def _set(self, obj, attr, value):
        if isinstance(attr, str):
            setattr(obj, attr, value)
        elif isinstance(attr, int):
            obj[attr] = value
        else:
            for a in attr[:-1]:
                obj = self._get(obj, a)
            self._set(obj, attr[-1], value)


class PointerByFn:

    def __init__(self, obj, reader, writer):
        self.obj = obj
        self.reader = reader
        self.writer = writer

    def set(self, value):
        self.writer(self.obj, value)

    def get(self):
        return self.reader(self.obj)


def make_pointer(obj, attr, update_callback=None):
    if (isinstance(attr, tuple) or isinstance(attr, list)) \
            and len(attr) == 2 \
            and callable(attr[0]) and callable(attr[1]):
                return PointerByFn(obj, *attr)
    return Pointer(obj, attr, update_callback)
