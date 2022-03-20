import math as m

from ..math import *

__all__ = ["Drop"]


def _map(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    """
    linear interpolation
    """
    return (y0 * (x1-x) + y1 * (x-x0)) / (x1-x0)


class Drop:

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        min_r: float,
        max_r: float,
        n: int = 360,
        squish: float = 10.,
        random_mesh: bool = False,
    ) -> None:
        self._pos = Vector(x, y, z)  # position of the center of the drop
        self._min_r = min_r  # minimum radius of the drop
        self._max_r = max_r  # maximum radius of the drop

        self._n = n  # number of points that will be generated along each axis

        self._points: list[Vector] = []  # list of points of the drop

        self._noise = PerlinNoise(4, unbias=True)  # perlin noise generator
        # self._noise = OpenSimplexNoise()  # open simplex noise generator
        self._t_off = 0.  # time offset for the noise
        self._squish = squish  # squish contant for the noise

        if random_mesh:
            self._generate_rd()
        else:
            self._generate_un()

    def _generate_un(self) -> None:
        self._points.clear()
        for i in range(self._n):
            theta = i * 2 * m.pi / self._n
            for j in range(self._n):
                phi = j * m.pi / self._n
                x = m.sin(theta) * m.cos(phi)
                y = m.sin(theta) * m.sin(phi)
                z = m.cos(theta)

                s = self._squish
                n = self._noise(x / s, y / s, z / s, self._t_off)
                r = _map(n, -1, 1, self._min_r, self._max_r)
                x *= r
                y *= r
                z *= r

                self._points.append(Vector(x, y, z) + self._pos)

    def _generate_rd(self) -> None:
        self._points.clear()
        for _ in range(self._n * self._n):
            v = Vector.random3d()
            x, y, z = v[::]

            s = self._squish
            n = self._noise(x / s, y / s, z / s, self._t_off)
            r = _map(n, -1, 1, self._min_r, self._max_r)
            x *= r
            y *= r
            z *= r

            self._points.append(Vector(x, y, z) + self._pos)

    def as_surface(self) -> tuple[list[float], list[float], list[float]]:
        """
        get the points of the drop as a surface

        Returns
        -------
        ```py
            tuple[list[float], list[float], list[float]] : x, y, z list of coordinates
        ```
        """
        x: list[float] = []
        y: list[float] = []
        z: list[float] = []
        for point in self._points:
            x.append(point.x)
            y.append(point.y)
            z.append(point.z)
        return x, y, z
