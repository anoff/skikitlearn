import matplotlib.pyplot as plt
import gpxpy.parser as parser
import datetime
import numpy as np


def smooth(y, box_pts=11):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def load_points(filename):
    gpx_file = open(filename, 'r')
    gpx_parser = parser.GPXParser(gpx_file)
    gpx_file.close()
    gpx = gpx_parser.parse()
    # aggregate all points into one array
    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append(point)
    return points

points = load_points('data/runtastic_20170322_1454_Skiing.gpx')
print("Points: {}".format(len(points)))
print(points[0])

times = [p.time for p in points]
t_min = min(times)
durations = [(t - t_min).total_seconds() for t in times]
heights = [p.elevation for p in points]
delta_h = np.diff(heights)
delta_h_filt = np.append(0, smooth(delta_h, 5))

delta_t = np.diff(durations)

v_z = delta_h_filt/np.append(0, delta_t)
plt.figure(1)
plt.subplot(311)
plt.hist(delta_t)
plt.ylabel("# deltaT")
plt.subplot(312)
plt.plot(durations, heights, durations, smooth(heights, 3),  durations, smooth(heights, 5),  durations, smooth(heights, 10))
plt.legend(["height", "s3", "s5", "s10"])
#plt.savefig('analysis.png', dpi=600)
#plt.show()


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
