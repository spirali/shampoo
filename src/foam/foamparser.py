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


import pyparsing as pp
import re
from foam.datatypes import FoamArray, FoamDict


class ParseError(Exception):
    pass

int_regex = re.compile(r'^[+-]?[0-9]+$')

lpar, rpar, sem, lcurly, rcurly \
    = map(pp.Suppress, "();{}")

string = pp.Word(pp.alphas+"_", pp.alphanums+"_") | \
        pp.dblQuotedString.setParseAction(lambda t: t[0][1:-1])
number = pp.Regex(r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?')

def make_number(t):
    v = t[0]
    if int_regex.match(v):
        return int(v)
    else:
        return float(v)
number.setParseAction(make_number)

value = pp.Forward()
key_value = pp.Group(string + value)

dictionary = pp.Forward()
dict_body = pp.ZeroOrMore(pp.Group(string + ((value + sem) | dictionary)))
dictionary << (lcurly + dict_body + rcurly)
array_begin = pp.Regex(r'[0-9]*\(')
array = array_begin + pp.Group(pp.ZeroOrMore(value)) + rpar
named_item = string + pp.Optional(array | dictionary, None)
value << (array | number | named_item)

oneline_comment = pp.Keyword("//") + pp.SkipTo(pp.LineEnd())

file_with_dictionary = pp.Suppress(pp.Keyword("FoamFile")) + dictionary + dict_body
file_with_dictionary.ignore(pp.cStyleComment)
file_with_dictionary.ignore(oneline_comment)

def make_dictionary(t):
    d = FoamDict()
    for key, value in t:
        d.add(key, value)
    return d
dict_body.setParseAction(make_dictionary)

def make_array(t):
    return FoamArray(t[1])
array.setParseAction(make_array)

def make_names_item(t):
    obj = t[1]
    if obj:
        obj.name = t[0]
        return obj
    else:
        return t[0]
named_item.setParseAction(make_names_item)
