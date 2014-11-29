from foamparser import value, dictionary, file_with_dictionary, \
                       FoamArray, FoamDict

def test_literals_strings():
    assert "one/t wo" == value.parseString("\"one/t wo\"", parseAll=True)[0]
    assert "_abc_cde_" == value.parseString("_abc_cde_", parseAll=True)[0]

def test_literals_numbers():
    assert 123.2 == value.parseString("123.2", parseAll=True)[0]
    assert 123 == value.parseString("123", parseAll=True)[0]
    assert -10e1 == value.parseString("-10e1", parseAll=True)[0]
    assert 10.21e-3 == value.parseString("10.21e-3", parseAll=True)[0]

def test_dictionary():
    assert FoamDict() == dictionary.parseString("{}", parseAll=True)[0]
    d = FoamDict()
    d.add("key1", 10)
    d.add("key2", "value")
    assert d == \
           dictionary.parseString("{ key1 10; key2 value; }", parseAll=True)[0]
    d = FoamDict()
    d.add("key2", FoamDict())
    d.add("key1", 10)
    d2 = FoamDict("key3")
    d2.add("a", 1)
    d2.add("b", 2)
    d.add("key3", d2)
    assert d == \
           dictionary.parseString("{ key2 {} key1 10; key3 { a 1; b 2; } }", parseAll=True)[0]

def test_array():
    assert FoamArray((10, 20)) == value.parseString("(10 20)", parseAll=True)[0]
    assert FoamArray() == value.parseString("()", parseAll=True)[0]
    assert FoamArray((10, 20)) == value.parseString("2(10 20)", parseAll=True)[0]
    assert FoamArray((FoamArray((10, 20)), FoamArray((5,)), FoamArray((7, 8, 9)))) == \
            value.parseString("((10 20) 1(5) (7 8 9))", parseAll=True)[0]
    assert FoamArray((1, 2, 3), "abc") == \
            value.parseString("abc (1 2 3)", parseAll=True)[0]
    assert FoamArray((1, 2, 3), "abc") == \
            value.parseString("abc 3(1 2 3)", parseAll=True)[0]
    assert FoamArray((1, FoamArray((1, 1), "cde"), 3), "abc") == \
            value.parseString("abc 3(1 cde 2(1 1) 3)", parseAll=True)[0]


def test_foamfile():
    string = """
        /* Foam file */
        FoamFile
        {
            version 2.0;
            format ascii;
            class dictionary;
            object blockMeshDict;
        }
        /* Content of the file */
        convertToMeters 1;
        vertices 8(
            (-1 -1 -1) // First vertex
            (1 -1 -1)
            (1 -1 1)
            (-1 -1 1)
            (-1 1 -1)
            (1 1 -1)
            (1 1 1)
            (-1 1 1)
        );
        blocks ( hex (0 1 2 3 4 5 6 7) (14 14 14 ) simpleGrading (1 1 1) );
        edges ();
        boundary ();
    """
    foam_file = FoamDict()
    foam_file.add("version", 2.0)
    foam_file.add("format", "ascii")
    foam_file.add("class", "dictionary")
    foam_file.add("object", "blockMeshDict")

    rest_of_file = FoamDict()
    rest_of_file.add("convertToMeters", 1)
    rest_of_file.add("vertices", FoamArray(((-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1),
                      (-1, 1, -1), (1, 1, -1), (1, 1, 1), (-1, 1, 1)), recursive=True))
    rest_of_file.add("blocks", FoamArray((FoamArray((0, 1, 2, 3, 4, 5, 6, 7), "hex"),
                               FoamArray((14, 14, 14)),
                               FoamArray((1, 1, 1), "simpleGrading"))))
    rest_of_file.add("edges", FoamArray())
    rest_of_file.add("boundary", FoamArray())
    header, content = file_with_dictionary.parseString(string, parseAll=True)
    assert foam_file == header
    assert rest_of_file == content
