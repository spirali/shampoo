
from base.geom import BoundingBox
import base.geom as geom

def test_bounding_box_reset():
    bbox = BoundingBox()
    assert not bbox.is_valid()
    bbox.add_point((100, 200, 300))
    assert bbox.is_valid()
    bbox.reset()
    assert not bbox.is_valid()

def test_bounding_box_add_point():
    bbox = BoundingBox()
    p0 = (150, 250, 350)
    bbox.add_point(p0)
    assert p0 == bbox.min_point
    assert p0 == bbox.max_point


    p1 = (100, 200, 300)
    p2 = (200, 300, 400)
    bbox.add_point(p1)
    bbox.add_point(p2)
    assert p1 == bbox.min_point
    assert p2 == bbox.max_point

    p3 = (150, 100, 500)
    bbox.add_point(p3)
    assert (100, 100, 300) == bbox.min_point
    assert (200, 300, 500) == bbox.max_point

def test_merge():
    bbox1 = BoundingBox()
    bbox1.add_point((100, 200, 300))
    bbox1.add_point((1000, 2000, 4000))
    bbox2 = BoundingBox()
    bbox2.add_point((50, 200, 350))
    bbox2.add_point((950, 2000, 4050))
    bbox = bbox1.merge(bbox2)
    assert bbox.min_point == (50, 200, 300)
    assert bbox.max_point == (1000, 2000, 4050)

def test_diameter():
    bbox = BoundingBox()
    bbox.add_point((100, 100, 300))
    bbox.add_point((200, 300, 400))

    assert bbox.size == (100, 200, 100)
    assert bbox.center == (150, 200, 350)
    assert bbox.diameter == 200

def test_normalize():
    assert geom.vec_length(geom.vec_normalize((10, 13, 11))) == 1
