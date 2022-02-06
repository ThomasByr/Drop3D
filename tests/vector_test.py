import math as m

from drop3d import *
from pytest import approx


def test_vector_0() -> None:
    v = Vector(1, 2, 3)
    assert v.x == 1


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
