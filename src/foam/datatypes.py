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


class FoamArray:

    def __init__(self, items=(), name=None, recursive=False):
        self.name = name
        self.items = list(items)
        if recursive:
            for i, item in enumerate(self.items):
                if isinstance(item, list) or isinstance(item, tuple):
                    self.items[i] = FoamArray(item, recursive=True)

    def clean_list(self):
        result = []
        for item in self.items:
            if isinstance(item, FoamArray):
                result.append(item.clean_list())
            else:
                result.append(item)
        return result

    def __iter__(self):
        return iter(self.items)

    def __eq__(self, other):
        return isinstance(other, FoamArray) \
                and other.name == self.name \
                and other.items == self.items

    def __neq__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "FoamArray({0}, {1})".format(repr(self.items), repr(self.name))


class FoamDict:

    def __init__(self, name=None):
        self.name = name
        self.items = []
        self.dicts = []

    def add(self, key, value):
        if isinstance(value, FoamDict):
            assert value.name is None or value.name == key
            value.name = key
            self.add_dict(value)
        else:
            self.items.append((key, value))

    def get(self, key):
        item = self._find_key(key)
        return item[1]

    def get_float(self, key):
        return float(self.get(key))

    def add_dict(self, dictionary):
        self.dicts.append(dictionary)

    def get_dict(self, name):
        for dictionary in self.dicts:
            if dictionary.name == name:
                return dictionary
        raise Exception("Dictionary '{0}' not found".format(name))

    def _find_key(self, key):
        for item in self.items:
            if item[0] == key:
                return item
        raise Exception("Item '{0}' not found".format(key))

    def __eq__(self, other):
        return isinstance(other, FoamDict) \
                and other.name == self.name \
                and other.items == self.items \
                and other.dicts == self.dicts

    def __neq__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
         return "FoamDict({0}, {1}, {2})".format(repr(self.name), repr(self.items), repr(self.dicts))

