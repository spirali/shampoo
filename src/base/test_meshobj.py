
from base.meshobj import MeshObject

def test_polygon():
    m = MeshObject()
    p1 = (0, 0, 0)
    p2 = (1, 0, 0)
    p3 = (1, 1, 0)
    p4 = (0.5, 2, 0)
    p5 = (-0.5, 1, 0)
    m.add_polygon([p1, p2, p3, p4, p5])
    assert len(m.vertices) == 9
