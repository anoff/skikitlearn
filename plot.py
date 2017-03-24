import matplotlib.pyplot as plt
from lib.process import load_points, calc_additional

points = load_points('data/runtastic_20170322_1454_Skiing.gpx')
duration, height, d_height, distance, d_distance = calc_additional(points)
print("Points: {}".format(len(points)))
#print(points)

x = duration
plt.figure(1)
plt.subplot(311)
plt.step(x, height)
plt.ylabel("height [m]")

plt.subplot(312)
plt.step(x, distance)
plt.ylabel("distance [m]")

plt.subplot(313)
plt.step(range(len(duration)), duration)
plt.show()


'''
plt.figure(3)
plt.scatter(-1, -1, c="r")
plt.scatter(-1, -1, c="b")
plt.scatter(-1, -1, c="y")
plt.legend(['going up', 'going down', 'not moving'])
for ix in range(len(durations)):
    if delta_h_filt[ix] > 0:
        c = 'r'
    elif delta_h_filt[ix] == 0:
        c = 'y'
    else:
        c = 'b'
    plt.scatter(durations[ix], heights[ix], c=c)
plt.plot(durations, v_z*36+2000, '--m')
plt.xlim([0, max(durations)])
plt.ylim([min(heights), max(heights)])
plt.xlabel('time [s]')
plt.ylabel('elevation [m]')
plt.savefig('plot.png', dpi=600)
'''
