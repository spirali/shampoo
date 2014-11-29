from base.pointers import make_pointer

def test_make_pointer_attribtue():
    class A:
        def __init__(self):
            self.x = 123
    a = A()
    p = make_pointer(a, "x")

    assert p.get() == 123
    p.set(200)
    assert p.get() == 200
    assert a.x == 200

def test_make_pointer_index():
    a = [ 123, 321, 231 ]
    p = make_pointer(a, 1)

    assert p.get() == 321
    p.set(200)
    assert p.get() == 200
    assert a == [ 123, 200, 231 ]

def test_make_pointer_complex():
    class A:
        pass
    a = A()
    c = A()
    c.x = "Hello"
    a.b = [ 0, 1, c, 1 ]

    p = make_pointer(a, ("b", 2, "x"))

    assert p.get() == "Hello"
    p.set("Fly")
    assert p.get() == "Fly"
    assert c.x == "Fly"

def test_pointer_by_fn():
    x = [None]

    def set_fn(obj, value):
        obj[0] = value

    def get_fn(obj):
        return obj[0]

    p = make_pointer(x, (get_fn, set_fn))

    p.set("X")
    assert p.get() == "X"

    p.set("Y")
    assert p.get() == "Y"
    assert x == ["Y"]
