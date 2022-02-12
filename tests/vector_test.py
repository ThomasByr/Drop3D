import math as m

from drop3d import *
from pytest import approx


def test_vector_0() -> None:
    v = Vector(1, 2, 3)
    assert v.x == 1
    assert v.y == 2
    assert v.z == 3


def test_vector_1() -> None:
    v = Vector(1)
    v.rotate(m.pi / 2)
    assert v.x == approx(0)
    assert v.y == approx(1)


def test_vector_2() -> None:
    v = Vector(1)
    a = v.get_angle()
    assert a == approx(0)

    v = Vector(1, 1)
    a = v.get_angle()
    assert a == approx(m.pi / 4)


def test_vector_3() -> None:
    v = Vector(1, 1).normalized()
    print(v)
    v.rotate(-m.pi / 4)
    print(v)
    assert v.x == approx(1)
    assert v.y == approx(0)


def test_vector_4() -> None:
    x = Vector(1)
    y = Vector(0, 1)
    z = Vector(0, 0, 1)

    assert x.dot(y) == approx(0)
    assert x.dot(z) == approx(0)
    assert y.dot(z) == approx(0)
    assert x.cross(y) == z
    assert y.cross(z) == x
    assert z.cross(x) == y


def test_vector_5() -> None:
    v = Vector.random3d()
    assert v.mag == approx(1)


def test_vector_6() -> None:
    v = Vector.random3d()
    x = Vector(1)
    y = Vector(0, 1)
    z = Vector(0, 0, 1)

    assert v.projected(x).x == approx(0)
    assert v.projected(y).y == approx(0)
    assert v.projected(z).z == approx(0)


def test_vector_7() -> None:
    v = Vector.random3d()
    w = Vector.random2d()
    z = Vector(0, 0, 1)

    a = b = c = 1
    x = (a*v + b*w) / c
    y = v @ w
    assert isinstance(x, Vector) == True
    assert isinstance(y, float) == True

    assert w.projected(z) == w
    assert v.projected(z).cross(w).x == approx(0)
    assert v.projected(z).cross(w).y == approx(0)
    assert v.projected(z).cross(w).z != approx(0)
