import matplotlib.pyplot as plt
import gpxpy
import datetime
import numpy as np
from collections import namedtuple
from scipy.signal import savgol_filter

def smooth(y, box_pts=11):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def load_points(filename):
    Point = namedtuple("Point", ["lon", "lat", "elevation", "distance", "time"])
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)
    gpx_file.close()
    # aggregate all points into one array
    points = []
    # print(dir(gpx.tracks[0].segments[0].points[0]))
    for track in gpx.tracks:
        for segment in track.segments:
            for index, point in enumerate(segment.points, start=0):
                new_point = Point(
                    lon=point.longitude,
                    lat=point.latitude,
                    elevation=point.elevation,
                    distance=point.distance_3d(segment.points[index-1]) if index > 0 else 0,
                    time=point.time
                )
                points.append(new_point)
    return points

points = load_points('data/runtastic_20170322_1454_Skiing.gpx')
print("Points: {}".format(len(points)))
#print(points)

times = [p.time for p in points]
t_min = min(times)
durations = [(t - t_min).total_seconds() for t in times]
heights = [p.elevation for p in points]
delta_h = np.diff(heights)
delta_h_filt = np.append(0, smooth(delta_h, 5))
distance = [p.distance for p in points]
delta_t = np.diff(durations)

v_z = delta_h_filt[1:]/delta_t # HACK remove one point to achieve same length
x = durations
plt.figure(1)
plt.subplot(311)
plt.plot(x, distance, x, smooth(distance, 3),  x, smooth(distance, 5),  x, smooth(distance, 11), x, savgol_filter(distance, 5, 2), x, savgol_filter(distance, 11, 2))
plt.legend(["distance", "s3", "s5", "s10", "sg5", "sg10"])

print("distance: {}, s3: {}, s5: {}, s10: {}, sg5: {}, sg10: {}".format(sum(distance), sum(smooth(distance, 3)), sum(smooth(distance, 5)), sum(smooth(distance, 11)), sum(savgol_filter(distance, 5, 2)), sum(savgol_filter(distance, 11, 2))))
plt.subplot(312)
plt.plot(x, heights, x, smooth(heights, 3),  x, smooth(heights, 5),  x, smooth(heights, 10))
plt.legend(["height", "s3", "s5", "s10"])
#plt.savefig('analysis.png', dpi=600)
plt.subplot(313)
plt.plot(x, distance)
plt.ylabel("distance")
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
