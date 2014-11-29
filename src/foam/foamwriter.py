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


from foam.datatypes import FoamDict, FoamArray


def is_atom(value):
    return isinstance(value, int) \
           or isinstance(value, float) \
           or isinstance(value, str)
class FoamWriter:

    def __init__(self, file):
        self.file = file
        self.indent = ""

    def new_line(self):
        self.file.write("\n" + self.indent)

    def indent_push(self):
        self.indent += "\t"

    def indent_pop(self):
        assert self.indent
        self.indent = str(self.indent[:-1])

    def write_value(self, obj):
        if isinstance(obj, int) or isinstance(obj, float):
            self.file.write(str(obj))
        elif isinstance(obj, FoamArray):
            self.write_array(obj)
        elif isinstance(obj, str):
            if not obj or not obj[0].isalpha() or not obj.isalnum():
                self.file.write("\"" + obj + "\"")
            else:
                self.file.write(obj)
        elif isinstance(obj, FoamDict):
            self.write_dictionary(obj)
        else:
            raise Exception("Value {0} cannot be written", repr(obj))

    def write_dictionary(self, obj):
        if obj.name is None:
            self.file.write("{")
        else:
            self.file.write("{0} {{".format(obj.name))
        self.indent_push()
        self.write_dictionary_body(obj)
        self.indent_pop()
        self.new_line()
        self.file.write("}")

    def write_dictionary_body(self, obj):
        for key, value in obj.items:
            self.new_line()
            self.file.write(key + " ")
            self.write_value(value)
            self.file.write(";")

        for dictionary in obj.dicts:
            self.new_line()
            self.write_dictionary(dictionary)

    def write_array(self, obj):
        if obj.name:
            self.file.write(obj.name + " ")
        items = obj.items
        if items and len(items) < 20 and is_atom(items[0]):
            self.file.write("(")
            self.write_value(items[0])
            for o in items[1:]:
                self.file.write(" ")
                self.write_value(o)
            self.file.write(")")
        elif items:
            self.file.write("{0}(".format(len(items)))
            self.indent_push()
            for o in items:
                self.new_line()
                self.write_value(o)
            self.indent_pop()
            self.new_line()
            self.file.write(")")
        else:
            self.file.write("()")
