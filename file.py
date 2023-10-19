""" walls = {
    (
        (20, 0), (30, 20)
    ),
    (
        (70, -5), (70, 25)
    )
    }
wallcount = {}
for wall in walls:
    wallcount.update({wall:0})
    wallcount.update({wall: wallcount[wall]+1})
    print(wallcount[wall])
print(wallcount) """
""" import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation
fig, ax = plt.subplots()
t = np.linspace(0, 3, 40)
g = -9.81
v0 = 12
z = g * t**2 / 2 + v0 * t

v02 = 5
z2 = g * t**2 / 2 + v02 * t

scat = ax.scatter(t[0], z[0], c="b", s=5, label=f'v0 = {v0} m/s')
line2 = ax.plot(t[0], z2[0], label=f'v0 = {v02} m/s')[0]
ax.set(xlim=[0, 3], ylim=[-4, 10], xlabel='Time [s]', ylabel='Z [m]')
ax.legend()


def update(frame):
    # for each frame, update the data stored on each artist.
    x = t[:frame]
    y = z[:frame]
    # update the scatter plot:
    data = np.stack([x, y]).T
    scat.set_offsets(data)
    # update the line plot:
    line2.set_xdata(t[:frame])
    line2.set_ydata(z2[:frame])
    return (scat, line2)


ani = animation.FuncAnimation(fig=fig, func=update, frames=40, interval=30)
plt.show() """
import matplotlib.pyplot as plt
plt.clf()
plt.axes().set_aspect('equal')
""" plt.plot(20,20,"r*",markersize=20.0) """
plt.plot([10,10],[40,20],"-k",linewidth=3)
var = plt.plot([20,10],[10,20],"-k",linewidth=3)
plt.draw()
plt.pause(1)
for e in var:
    e.remove()
plt.draw()
plt.pause(1)
