from enum import Enum
from typing import Any, Iterable

import random as r

from ..core import *

__all__ = [
    "GenMode", "MeshMode", "gen_mode", "mesh_mode", "precision", "squish", "scene", "create_drop",
    "each_drop", "as_surface"
]


class GenMode(Enum):
    """
    Control of the generation method for drops\\
    `RANDOM` - will generate a drop at a random position\\
    `FIXED` - will generate a drop at a specified position
    """
    RANDOM = "random"
    FIXED = "fixed"


class MeshMode(Enum):
    """
    Control of the method to generate points on the surface of the drop\\
    `RANDOM` - will generate a point at a random position\\
    `FIXED` - will generate a point at a specified position
    """
    UNIFORM = "uniform"
    RANDOM = "random"


_precision = 360
_squish = 10.
_gen_mode = GenMode.FIXED
_mesh_mode = MeshMode.UNIFORM
_scene = [[-1., 1.], [-1., 1.], [-1., 1.]]

_drops: list[Drop] = []
_drops_id: list[int] = []


def _get_params(*args, **kwargs) -> dict[str, Any]:
    """
    get parameters and name them
    """
    params: dict[str, Any] = {}

    l: list[str] = ["min_r", "max_r"]

    # if _gen_mode == GenMode.RANDOM:
    #     params["x"] = r.uniform(_scene[0][0], _scene[0][1])
    #     params["y"] = r.uniform(_scene[1][0], _scene[1][1])
    #     params["z"] = r.uniform(_scene[2][0], _scene[2][1])
    # elif _gen_mode == GenMode.FIXED:
    #     l = ["x", "y", "z", "min_r", "max_r"]
    # else:
    #     raise ValueError("invalid generation mode")
    
    match _gen_mode:
        case GenMode.RANDOM:
            params["x"] = r.uniform(_scene[0][0], _scene[0][1])
            params["y"] = r.uniform(_scene[1][0], _scene[1][1])
            params["z"] = r.uniform(_scene[2][0], _scene[2][1])
        case GenMode.FIXED:
            l = ["x", "y", "z", "min_r", "max_r"]
        case _:
            raise ValueError("invalid generation mode")

    i = 0
    for arg in l:
        params[arg] = kwargs.get(arg, None)
        if params[arg] is None:
            try:
                params[arg] = args[i]
                i += 1
            except IndexError:
                raise ValueError(f"{arg} is required")

    params["n"] = _precision
    params["squish"] = _squish
    params["random_mesh"] = _mesh_mode == MeshMode.RANDOM
    return params


def gen_mode(mode: GenMode = None) -> None | GenMode:
    """
    set the generation mode\\
    if called with no arguments, returns the current generation mode

    Parameters
    ----------
    ```py
        mode : GenMode
            RANDOM | SEQUENTIAL
    ```
    """
    global _gen_mode
    if mode is None:
        return _gen_mode
    _gen_mode = mode


def mesh_mode(mode: MeshMode = None) -> None | MeshMode:
    """
    set the surface generation mode\\
    if called with no arguments, returns the current mesh mode

    Parameters
    ----------
    ```py
        mode : MeshMode
            UNIFORM | RANDOM
    ```
    """
    global _mesh_mode
    if mode is None:
        return _mesh_mode
    _mesh_mode = mode


def precision(n: int = None) -> None | int:
    """
    set the precision of the drop\\
    if called with no arguments, returns the current precision

    Parameters
    ----------
    ```py
        n : int, (optional)
            number of points along each axis
            defaults to None
    ```
    """
    global _precision
    if n is None:
        return _precision
    _precision = n


def squish(s: float = None) -> None | float:
    """
    set the amount of noise for the drop\\
    if called with no arguments, returns the current squish constant
    
    Parameters
    ----------
    ```py
        s : float, (optional)
            a higher value will make the drop more spherical
            defaults to None
    ```
    """
    global _squish
    if s is None:
        return _squish
    _squish = s


def scene(
    x_min: float = None,
    x_max: float = None,
    y_min: float = None,
    y_max: float = None,
    z_min: float = None,
    z_max: float = None,
) -> None | list[list[float]]:
    """
    set the scene (the range for the drops generation)\\
    if called with no arguments, returns the current scene
    
    Parameters
    ----------
    ```py
        x_min : float, (optional)
            minimum x value
            defaults to None
        x_max : float, (optional)
            maximum x value
            defaults to None
        y_min : float, (optional)
            minimum y value
            defaults to None
        y_max : float, (optional)
            maximum y value
            defaults to None
        z_min : float, (optional)
            minimum z value
            defaults to None
        z_max : float, (optional)
            maximum z value
            defaults to None
    ```
    """
    global _scene
    if x_min is None and x_max is None and y_min is None and y_max is None and z_min is None and z_max is None:
        return _scene
    x_min = _scene[0][0] if x_min is None else x_min
    x_max = _scene[0][1] if x_max is None else x_max
    y_min = _scene[1][0] if y_min is None else y_min
    y_max = _scene[1][1] if y_max is None else y_max
    z_min = _scene[2][0] if z_min is None else z_min
    z_max = _scene[2][1] if z_max is None else z_max
    _scene = [[x_min, x_max], [y_min, y_max], [z_min, z_max]]


def create_drop(*args, **kwargs) -> None:
    """
    create a drop\\
    depending on the generation mode, the drop will be generated at a random position or at a specified position

    Parameters
    ----------
    ```py
        x : float, (optional)
            x position of the center of the drop
        y : float, (optional)
            y position of the center of the drop
        z : float, (optional)
            z position of the center of the drop
        min_r : float
            minimum radius
        max_r : float
            maximum radius
    ```
    """
    global _drops, _drops_id

    params = _get_params(*args, **kwargs)
    drop: Drop = Drop(**params)
    _drops.append(drop)
    _drops_id.append(len(_drops) - 1)


def each_drop() -> Iterable[int]:
    """
    Iterate over all drops
    """
    global _drops
    for drop in _drops_id:
        yield drop


def as_surface(drop: int = None) -> tuple[list[float], list[float], list[float]]:
    """
    get the points of the drop as a surface\\
    if called with no arguments, returns the points of the last drop created

    Parameters
    ----------
    ```py
        drop : int, (optional)
            drop id
            defaults to None
    ```

    Returns
    -------
    ```py
        tuple[list[float], list[float], list[float]] : x, y, z list of coordinates
    ```
    """
    global _drops, _drops_id
    if drop is None:
        drop = _drops_id[-1]
    return _drops[drop].as_surface()
