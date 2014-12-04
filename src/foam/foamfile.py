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


from foam.foamparser import file_with_dictionary
from foam.foamwriter import FoamWriter
from foam.datatypes import FoamDict
import base.paths as paths

import os
import logging


shampoo_logo = """/*    ___ _                                              *\\
|    / __| |_  __ _ _ __  _ __  ___  ___                  |
|    \__ \ ' \/ _` | '  \| '_ \/ _ \/ _ \                 |
|    |___/_||_\__,_|_|_|_| .__/\___/\___/                 |
\*                v0.0.1 |_| http://TODO                 */
"""


class FoamFile:

    def __init__(self, filename):
        self.filename = filename
        self.header_dict = {}
        self.content = None

    def read_as_dictionary(self):
        logging.debug("Reading OpenFoam file '%s'", self.filename)
        self.header_dict, self.content = \
                file_with_dictionary.parseFile(self.filename, parseAll=True)

    def write_dictionary(self, value):
        logging.debug("Writing OpenFoam file '%s'", self.filename)
        assert self.header_dict
        paths.makedir_if_not_exists(os.path.dirname(self.filename))
        with open(self.filename, "w") as f:
            f.write(shampoo_logo)
            f.write("\n")
            fw = FoamWriter(f)
            fw.write_dictionary(self.header_dict)
            f.write("\n\n")
            fw.write_dictionary_body(value)

    def set_header_dict(self, class_name, object_name):
        self.header_dict = FoamDict("FoamFile")
        self.header_dict.add("version", 2.0)
        self.header_dict.add("format", "ascii")
        self.header_dict.add("class", class_name)
        self.header_dict.add("object", object_name)
