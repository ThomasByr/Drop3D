# Drop3D

> A 3d water drop simulator

1. [Building the library](#building-the-library)
2. [Small helpme doc](#small-helpme-doc)
3. [Changelog](#changelog)
4. [TODO](#todo)

This library allows the user to easily create and export the data describing the surface of a pseudo-randomly generated 3D drop of liquid.

## Building the library

You will need `wheel` and `build` package installed with pip. Depending on whether you are running on Linux you may want to specify `python3` or `python3 -m`:

```ps1
python setup.py sdist bdist_wheel
```

You can then install with

```ps1
pip install dist/drop3d-[version]-py3-none-any.whl
```

## Small helpme doc

Bellow are functions declared in [userspace](drop3d/imports/userspace.py) file that the user can access when importing Drop3D.

<details>
<summary>gen_mode</summary>

```py
def gen_mode(mode: GenMode = None) -> None | GenMode
```

This is used to set the generation mode of the drops (because chances are you are going to generate many drops). The user can choose between a random spacial distribution of the drop (only the center will be randomly generated), or a manual distribution. When choosing to generate drops randomly, the range of the center of the drops will be picked inside of a given scene (see `scene` function).

If this function is called without any argument, it will simply return the current generation mode (as an enum from `GenMode`).
</details>

<details>
<summary>mesh_mode</summary>

```py
def mesh_mode(mode: MeshMode = None) -> None | MeshMode
```

This is used to set the generation mode of the drops mesh surface. The user can choose between a random spacial distribution of the surface points, or a more uniform distribution. When choosing to generate surface points randomly, there is no guaranty that the surface won't have any holes in it. If so, please consider boosting the precision of the drop (see `precision` function).

If this function is called without any argument, it will simply return the current mesh generation mode (as an enum from `MeshMode`).
</details>

<details>
<summary>precision</summary>

```py
def precision(n: int = None) -> None | int
```

This is used to specify the number of points generated along each axis, meaning, the actual drop will consist of `n*n` points (because we only use 2 axis to generate a sphere `(r, theta, phi)`. Default is 360, which will result in a lot of points. This is okay to export data (lets say to Blender for example) but can be quite slow if the goal is to visualise the drop in a cpu-base window.

If this function is called without any argument, it will simply return the current precision (as an integer).
</details>

<details>
<summary>squish</summary>

```py
def squish(s: float = None) -> None | float
```

This is used to set the "squish constant" for the noise generation algorithm (we use Perlin noise here). The bigger the constant, the more spherical the drop. Also note that the noise will interpolate between 2 radii to create "lumps" on the surface of the drop. A value of `n` mean we take the noise values from a sphere of radius `1/n` in the noise space.

If this function is called without any argument, it will simply return the current constant (as a floting point number).
</details>

<details>
<summary>scene</summary>

```py
def scene(x_min: float = None, x_max: float = None, y_min: float = None, y_max: float = None, z_min: float = None, z_max: float = None) -> None | list[list[float]]
```

This is used to set the scene when randomly generating drops. The center of each drop will be randomly picked in the respective range for each axis. The distribution is here uniform.

If this function is called without any argument, it will simply return the current scene (as a list of lists of floating point numbers).

</details>

<details>
<summary>create_drop</summary>

```py
def create_drop(*args, **kwargs) -> None
```

This is quite an important function. This one is used to actually generate a drop. The arguments may vary depending on the generation method, and can be ordered as following : `(x, y, z), min_r, max_r`, which stand for the xyz position of the center of the drop (which is not always required), the minimum and the maximum radius of the drop (which will create bigger "lumps" on the surface of the drop).

This function does not return anything and can throw `ValueError` when not called with the expected arguments.

</details>

<details>
<summary>each_drop</summary>

```py
def each_drop() -> Iterable[int]
```

This function is used to iterate over all generated drops as follow : `for drop in each_drop():` were the local variable `drop` will be an integer (holding the id of the drop). In all honesty, this is because we do not want the user to directly use or interfere with the Drop class (which is not accessible).

This function returns an iterator that yields intergers.

</details>

<details>
<summary>as_surface</summary>

```py
def as_surface(drop: int = None) -> tuple[list[float], list[float], list[float]]
```

This function is used to export data of a yielded drop id (see `each_drop` function). The user can get a list of coordinates in the form (xs, ys, zs) where .s holds a list of floating point numbers. Basically, xs[i] ,ys[i], z[i] are the 3d coordinates of the i-th generated drop.

This function returns a tuple of 3 lists containing floating point numbers.

</details>

## Changelog

*   initial push on github, the library is not yet available on the python package index
*   update on the vector class (which is accessible by the user for now)

## TODO

*   animate the drop (time offset)
*   set textures and normal map
