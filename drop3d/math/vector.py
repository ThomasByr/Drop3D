from collections import namedtuple
import random
import math as m
import re
from typing import NewType, Type
import numpy as np

__all__ = ["Vector"]

# Floating point precision for vectors.
EPSILON = 1e-8

Point = namedtuple("Point", ["x", "y", "z"])
Point.__new__.__defaults__ = (0, 0, 0)

Vector = NewType("Vector", Point)


class Vector(np.ndarray):
    """
    Vector
    ======
    provides :
    1. Vector support for `python 3.10` and upper in two or three dimensional space
    2. Fast standards operations using numpy
    3. Full random support plus ndarray and p5 compatibility

    A Vector -- specifically an Euclidean (or geometric) vector -- in
    two or three dimensional space is a geometric entity that has some
    magnitude (or length) and a direction.

    Examples
    --------
        >>> zero = Vector()
        >>> zero
        Vector(0.00, 0.00, 0.00)

        >>> vec_2d = Vector(3, 4)
        >>> vec_2d
        Vector(3.00, 4.00, 0.00)

        >>> vec_3d = Vector(2, 3, 4)
        >>> vec_3d
        Vector(2.00, 3.00, 4.00)

    Parameters
    ----------
    ```py
        x : int | float
            the x-component of the vector
        y : int | float
            the y-component of the vector
        z : int | float
            the z-component of the vector
    ```
    """

    def __new__(cls, *args: int | float) -> Vector:
        """
        new Vector instance

        Parameters
        ----------
        ```py
            args : tuple[int | float]
                coordinates of the Vector, unnamed
        ```

        Returns
        -------
        ```py
            Vector : new vector entity
        ```
        """
        assert not (n := len(args)) >= 4, "illegal dimension"
        (a := [e for e in args]).extend([0 for _ in range(3 - n)])
        obj = np.asarray(a, dtype=np.float64).view(cls)
        return obj

    def __eq__(self, other: Vector) -> bool:
        if self.shape == other.shape:
            return bool(np.all(np.absolute(self - other) <= EPSILON))
        return False

    def __ne__(self, other: Vector) -> bool:
        if self.shape == other.shape:
            return bool(np.any(np.absolute(self - other) > EPSILON))
        return True

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        fvalues = (class_name, self.x, self.y, self.z)
        return "{}({:.2f}, {:.2f}, {:.2f})".format(*fvalues)

    def __add__(self, other: Vector) -> Vector:
        return super().__add__(other)

    def __sub__(self, other: Vector) -> Vector:
        return super().__sub__(other)

    def __mul__(self, other: int | float | Vector) -> Vector:
        return super().__mul__(other)

    def __rmul__(self, other: int | float | Vector) -> Vector:
        return super().__rmul__(other)

    def __matmul__(self, other: Vector) -> float:
        return self.dot(other)

    def __rmatmul__(self, other: Vector) -> float:
        return self.dot(other)

    def __truediv__(self, other: int | float | Vector) -> Vector:
        return super().__truediv__(other)

    def __floordiv__(self, other: int | float | Vector) -> Vector:
        return super().__floordiv__(other)

    def __rtruediv__(self, other: int | float | Vector) -> Vector:
        return super().__truediv__(other)

    def __rfloordiv__(self, other: int | float | Vector) -> Vector:
        return super().__floordiv__(other)

    @property
    def x(self) -> float:
        """
        the x-component of the point
        """
        return self[0]

    @x.setter
    def x(self, value: float) -> None:
        self[0] = value

    @property
    def y(self) -> float:
        """
        the y-component of the point
        """
        return self[1]

    @y.setter
    def y(self, value: float) -> None:
        self[1] = value

    @property
    def z(self) -> float:
        """
        the z-component of the point
        """
        return self[2]

    @z.setter
    def z(self, value: float) -> None:
        self[2] = value

    def __getitem__(
        self,
        key: int | slice,
    ) -> int | float | np.ndarray:

        if isinstance(key, slice):
            return np.array([self[i] for i in range(*key.indices(len(self)))])
        return super().__getitem__(key)

    def __setitem__(
        self,
        key: int | slice,
        value: int | float | list[int | float],
    ) -> None:
        if isinstance(key, slice):
            for i, v in zip(range(*key.indices(len(self))), value):
                self[i] = v
        else:
            super().__setitem__(key, value)

    def __delitem__(
        self,
        key: int | slice,
    ) -> None:
        if isinstance(key, slice):
            for i in range(*key.indices(len(self))):
                del self[i]
        else:
            super().__delitem__(key)

    def getCoord(self, get: str = "xyz") -> np.ndarray:
        """
        Returns the coordinates of a Vector in a numpy array

        Parameters
        ----------
        ```py
            get : str, (optional)
                an ordered string of "x"s, "y"s, "z"s
                defaults to "xyz"
        ```

        Returns
        -------
        ```py
            np.ndarray : coordinates
        ```
        """
        l = {"x": 0, "y": 1, "z": 2, "X": 0, "Y": 1, "Z": 2}
        keys = l.keys()
        get = [e for e in get if e in keys]
        return np.array([self[l[e]] for e in get], dtype=np.float64)

    def setCoord(self, x: float = None, y: float = None, z: float = None) -> None:
        """
        Modifies the coordinates of the current Vector

        Parameters
        ----------
        ```py
            x : float, (optional)
                the x-component
            y : float, (optional)
                the y-component
            z : float, (optional)
                the z-component
        ```
        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        if z is None:
            z = self.z
        self.x, self.y, self.z = x, y, z

    def lerp(self, other: Vector, amount: float) -> Vector:
        """
        Linearly interpolate from one point to another

        Parameters
        ----------
        ```py
            other : Vector
                Point to be interpolate to
            amount: float
                Amount by which to interpolate.
        ```

        Returns
        -------
        ```py
            Vector : obtained by linearly interpolating this
                vector to the other vector by the given amount
        ```
        """
        x, y, z = self + amount * (other-self)
        return self.__class__(x, y, z)

    def rounded(self, ndigits: int = 0) -> Vector:
        """
        Returns a Vector whom cordinates has been rounded with the given precision

        Parameters
        ----------
        ```py
            ndigits : int
                number of digits to keep, may be negative
        ```

        Returns
        -------
        ```py
            Vector : new Vector
        ```
        """
        x, y, z = self
        return self.__class__(round(x, ndigits), round(y, ndigits), round(z, ndigits))

    def round(self, ndigits: int = 0) -> None:
        """
        Modifies the Vector and rounds its coordinates\\
        Does not return anything

        Parameters
        ----------
        ```py
            ndigits : int
                number of digits to keep, may be negative
        ```
        """
        self.x, self.y, self.z = tuple(map(lambda x: round(x, ndigits), self))

    def inverted(self) -> Vector:
        """
        Returns a Vector whom coordinates have been inverted, i.e. raised to power -1\\
        you might want to call `catch_inf` afterwards

        Returns
        -------
        ```py
            Vector : new Vector
        ```
        """
        return self.__class__(*1 / self)

    def invert(self) -> None:
        """
        Modifies the Vector and invert each coordinate\\
        deal with possible division by 0 warning
        """

        def invert(x: float) -> float:
            return x if abs(x) < EPSILON else 1 / x

        self.x, self.y, self.z = tuple(map(invert, self))

    def catch_inf(self) -> None:
        """
        Modifies the Vector and change inf coordinates to 0
        """

        def catch(x: float) -> float:
            return x if bool(x < np.inf) else 0

        self.x, self.y, self.z = tuple(map(catch, self))

    def cross(self, other: Vector) -> Vector:
        """
        Return the cross product of the two vectors

        Examples
        --------
            >>> i = Vector(1, 0, 0)
            >>> j = Vector(0, 1, 0)
            >>> i.cross(j)
            Vector(0.00, 0.00, 1.00)

        Parameters
        ----------
        ```py
            other : Vector
        ```

        Returns
        -------
        ```py
            Vector : The vector perpendicular to both `self` and `other`
                i.e., the vector obtained by taking the cross product of
                `self` and `other`
        ```
        """
        x, y, z = np.cross(self, other)
        return self.__class__(x, y, z)

    def dot(self, other: Vector) -> float:
        """
        Computes the dot product of two vectors

        Examples
        --------
            >>> p = Vector(2, 3, 6)
            >>> q = Vector(3, 4, 5)
            >>> p.dot(q)
            48
            >>> p @ q
            48

        Parameters
        ----------
        ```py
            other : Vector
        ```

        Returns
        -------
        ```py
            float : the dot product of the two vectors
        ```
        """
        return np.dot(self, other)

    @classmethod
    def random(cls, v1: float, v2: float, size: int = 3, dtype: Type[int | float] = float) -> Vector:
        """
        Creates a random generated Vector\\
        both `v1` and `v2` are included

        Examples
        --------
            >>> v1 = Vector.random(3, 10, size=2, dtype=int)
            >>> v2 = Vector.random(3, 10, size=2, dtype=float)
            >>> print(v1, v2, sep="\\n")
            ... # Vector(9.00, 7.00, 0.00)
            ... # Vector(7.88, 8.91, 0.00)

        Parameters
        ----------
        ```py
            v1 : float or int
                the minimum value
            v2 : float or int
                the maximum value
            size : int, (optional)
                the number of random-generated coordinates : min=0 | max=3
                defaults to 3
            dtype : type, (optional)
                the type of data : float or int
                defaults to float
        ```

        Returns
        -------
        ```py
            Vector : a new Vector
        ```
        """
        assert not ((size := abs(size)) >= 4), "please enter valid size"
        f = random.uniform if dtype is float else random.randint
        cast = float if dtype is float else int
        x, y, z = 0, 0, 0
        if size >= 1:
            x = f(cast(v1), cast(v2))
        if size >= 2:
            y = f(cast(v1), cast(v2))
        if size == 3:
            z = f(cast(v1), cast(v2))
        return cls(x, y, z)

    @classmethod
    def random2d(cls, mag: float = 1) -> Vector:
        """
        Generates a random 2d vector with an optional desired magnitude
        """
        x, y = 2 * (np.random.random(2) - 0.5)
        vec = cls(x, y)
        vec.magnitude = mag
        return vec

    @classmethod
    def random3d(cls, mag: float = 1) -> Vector:
        """
        Generates a random 3d vector with an optional desired magnitude
        """
        x, y, z = 2 * (np.random.random(3) - 0.5)
        vec = cls(x, y, z)
        vec.magnitude = mag
        return vec

    def copy(self) -> Vector:
        """
        Return a copy of the current point

        Returns
        -------
        ```py
            Vector : a copy of the current point
        ```
        """
        x, y, z = self
        return self.__class__(x, y, z)

    @property
    def magnitude(self) -> float:
        """
        The magnitude of the vector

        Examples
        --------
            >>> p = Vector(2, 3, 6)
            >>> p.magnitude
            7.0

            >>> abs(p)
            7.0

            >>> p.magnitude = 14
            >>> p
            Vector(4.00, 6.00, 12.00)

            >>> p.normalize()
            >>> print(p)
            Vector(0.29, 0.43, 0.86)
        """
        return m.sqrt(np.dot(self, self))

    @magnitude.setter
    def magnitude(self, value: float) -> None:
        if not (m := self.magnitude) == 0:
            self *= abs(value) / m

    @property
    def magnitude_sq(self) -> float:
        """
        The squared magnitude of the vector
        """
        return np.dot(self, self)

    @magnitude_sq.setter
    def magnitude_sq(self, value: float) -> None:
        self.magnitude = m.sqrt(value)

    def __abs__(self) -> float:
        return self.magnitude

    def normalize(self) -> None:
        """
        Sets the magnitude of the vector to 1
        """
        assert not self.magnitude == 0, "vector has magnitude 0, can't normalize"
        self.magnitude = 1

    def normalized(self) -> Vector:
        """
        Returns a copy of the current vector with a magnitude of 1
        """
        assert not self.magnitude == 0, "vector has magnitude 0, can't normalize"
        other = self.copy()
        other.magnitude = 1
        return other

    def limit(self, upper: float = None, lower: float = None) -> None:
        """
        Keeps the vector magnitude under or above a given limit
        """
        m = self.magnitude

        if lower is None:
            lower = m
        if upper is None:
            upper = m

        if m < lower:
            self.magnitude = lower
        elif m > upper:
            self.magnitude = upper

    def limited(self, upper: float = None, lower: float = None) -> Vector:
        """
        Returns a new vector whom magnitude has been kept under or above a given limit
        """
        other = self.copy()
        m = other.magnitude
        if lower is None:
            lower = m
        if upper is None:
            upper = m

        if m < lower:
            other.magnitude = lower
        elif m > upper:
            other.magnitude = upper
        return other

    def distance(self, other: Vector) -> float:
        """
        Return the distance between two points

        Parameters
        ----------
        ```py
            other : Vector
                other vector
        ```

        Returns
        -------
        ```py
            float : The distance between the current point and the given point
        ```
        """
        return m.sqrt(sum((v := (self - other)) * v))

    def distance_sq(self, other: Vector) -> float:
        """
        Return the squared distance between two points

        Parameters
        ----------
        ```py
            other : Vector
                other vector
        ```

        Returns
        -------
        ```py
            float : The squared distance between the current point and the given point
        ```
        """
        return sum((v := (self - other)) * v)

    @classmethod
    def _get_axis(cls, axis: str | Vector = "z") -> Vector:
        if isinstance(axis, str):
            axis = axis.lower()
            if axis == "x":
                axis = Vector(1, 0, 0)
            elif axis == "y":
                axis = Vector(0, 1, 0)
            elif axis == "z":
                axis = Vector(0, 0, 1)
            else:
                raise ValueError(f"invalid axis: {axis}")
        elif not isinstance(axis, Vector):
            raise ValueError(f"axis of invalid type {type(axis)}")

        return axis

    @classmethod
    def _next_axis(cls, axis: Vector) -> Vector:
        if axis == Vector(1, 0, 0):
            return Vector(0, 1, 0)
        elif axis == Vector(0, 1, 0):
            return Vector(0, 0, 1)
        elif axis == Vector(0, 0, 1):
            return Vector(1, 0, 0)
        return None

    def project(self, axis: str | Vector = "z") -> None:
        """
        project the new vector against the given axis\\
        meaning that the vector will be perpendicular to the given axis\\
        please provide an axis vector (or a string) of unit length 1

        Parameters
        ----------
        ```py
            axis : str | Vector, (optional)
                axis
                defaults to "z"
        ```
        """
        axis = self._get_axis(axis)
        v = self.dot(axis) * axis
        self -= v

    def projected(self, axis: str | Vector = "z") -> Vector:
        """
        project the vector against the given axis and return a new vector\\
        meaning that the vector will be perpendicular to the given axis\\
        please provide an axis vector (or a string) of unit length 1

        Parameters
        ----------
        ```py
            axis : str | Vector, (optional)
                axis
                defaults to "z"
        ```

        Returns
        -------
        ```py
            Vector : new Vector
        ```
        """
        axis = self._get_axis(axis)
        v = self.dot(axis) * axis
        return self - v

    def get_angle(self, axis: str | Vector = "z") -> float:
        """
        get the angle of the vector with respect to the given axis\\
        please provide an axis vector or a string of unit length 1

        Parameters
        ----------
        ```py
            axis : str | Vector, (optional)
                axis vector or string of unit length 1
                defaults to "z"
        ```

        Returns
        -------
        ```py
            float : angle in radians
        ```
        """
        axis = self._get_axis(axis)
        v = self.projected(axis)
        base = self._next_axis(axis)
        return np.arccos(np.dot(v, base) / v.magnitude)

    def set_angle(self, angle: float, axis: str | Vector = "z") -> None:
        """
        set the angle of the vector with respect to the given axis\\
        please provide an axis vector or a string of unit length 1

        Parameters
        ----------
        ```py
            angle : float
                angle in radians
            axis : str | Vector, (optional)
                axis vector or string of unit length 1
                defaults to "z"
        ```
        """
        axis = self._get_axis(axis)
        self.rotate(angle - self.get_angle(axis), axis)

    def rotate(self, angle: float, axis: str | Vector = "z") -> None:
        """
        rotate the current vector by a given angle in randians

        Parameters
        ----------
        ```py
            angle : float
                angle in radians
            axis : str | Vector, (optional)
                axis to rotate around
                defaults to "z"
        ```
        """
        axis = self._get_axis(axis)
        sin, cos = m.sin(angle), m.cos(angle)
        self[:] = cos*self + sin * axis.cross(self) + (1-cos) * axis * axis.dot(self)

    def rotated(self, angle: float, axis: str | Vector = "z") -> Vector:
        """
        return a new vector which have been rotated by a given angle in randians

        Parameters
        ----------
        ```py
            angle : float
                angle in radians
            axis : str | Vector, (optional)
                axis to rotate around
                defaults to "z"
        ```

        Returns
        -------
        ```py
            Vector : the rotated vector
        ```
        """
        axis = self._get_axis(axis)
        sin, cos = m.sin(angle), m.cos(angle)
        return cos*self + sin * axis.cross(self) + (1-cos) * axis * axis.dot(self)

    def angle_between(self, other: Vector) -> float:
        """
        Calculate the angle between two vectors

        Examples
        --------
            >>> from math import degrees
            >>> k = Vector(0, 1)
            >>> j = Vector(1, 0)
            >>> degrees(k.angle_between(j))
            90.0

        Parameters
        ----------
        ```py
            other : Vector
        ```

        Returns
        -------
        ```py
            float : The angle between two given vectors (in radians)
        ```
        """
        return np.arccos((np.dot(self, other)) / (self.magnitude * other.magnitude))

    @classmethod
    def from_angle(cls, angle: float) -> Vector:
        """
        Return a new unit vector with the given angle

        Parameters
        ----------
        ```py
            angle : float
                Angle to be used to create the vector (in radians)
        ```
        """
        vec = cls.random2d(mag=1)
        vec.angle = angle
        return vec

    # aliases
    __str__ = __repr__
    mag = norm = magnitude
    mag2 = magnitude_sq
    dist = distance
    dist_sq = distance_sq
    get_heading = get_angle
    u = phi = p = x
    v = theta = q = y
    w = psi = r = z
