import matplotlib.pyplot as plt

from drop3d import *

gen_mode(GenMode.FIXED)
mesh_mode(MeshMode.RANDOM)
precision(30)
squish(1)

create_drop(x=0, y=0, z=0, min_r=9, max_r=11)

plt.close()
plt.clf()
plt.cla()
fig = plt.figure(0)
ax = fig.add_subplot(111, projection="3d")

for drop in each_drop():
    x, y, z = as_surface(drop)
    ax.scatter(x, y, z)

# plt.show()
