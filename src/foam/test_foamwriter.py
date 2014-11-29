from foamparser import value, dict_body, FoamDict, FoamArray
from foamwriter import FoamWriter

import io


def io_get(f):
    f.seek(0)
    return f.read()

def test_write_array():
    s = io.StringIO()
    fw = FoamWriter(s)
    fw.write_value(FoamArray((10, 20)))
    assert io_get(s) == "(10 20)"

    s = io.StringIO()
    fw = FoamWriter(s)
    fw.write_value(FoamArray((10, 20), "xyz"))
    assert io_get(s) == "xyz (10 20)"

    s = io.StringIO()
    fw = FoamWriter(s)
    fw.write_value(FoamArray(range(100)))
    assert value.parseString(io_get(s), True)[0] == FoamArray(range(100))


def test_write_dict():
    d = { "int" : 100,
          "str" : "something/here",
          "arr" : (10, 20),
          "dict" : { "a" : 20, "b" : 30 } }
    d = FoamDict()
    d.add("int", 100)
    d.add("str", "something/here")
    d.add("arr", FoamArray((10, 20)))
    d2 = FoamDict()
    d2.add("a", 20)
    d2.add("b", 30)
    d.add("dict", d2)
    s = io.StringIO()
    fw = FoamWriter(s)
    fw.write_dictionary_body(d)
    assert dict_body.parseString(io_get(s), True)[0] == d
