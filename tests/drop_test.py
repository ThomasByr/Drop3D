import matplotlib.pyplot as plt

from drop3d import *

scene(-100, 100, -100, 100, -100, 100)
print(scene())
gen_mode(GenMode.RANDOM)
mesh_mode(MeshMode.UNIFORM)
precision(20)
squish(1)

for _ in range(100):
    create_drop(min_r=9, max_r=11)

plt.close("all")
plt.clf()
plt.cla()

fig = plt.figure(0)
ax = fig.add_subplot(111, projection="3d", aspect="auto")

for drop in each_drop():
    x, y, z = as_surface(drop)
    ax.scatter(x, y, z)

# plt.show()
