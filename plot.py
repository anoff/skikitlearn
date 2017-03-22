import matplotlib.pyplot as plt
import gpxpy.parser as parser
import datetime
import numpy as np


def smooth(y, box_pts=11):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

gpx_file = open( 'data/runtastic_20170322_1146_Skiing.gpx', 'r' )

gpx_parser = parser.GPXParser( gpx_file )
gpx = gpx_parser.parse()

gpx_file.close()

print("Tracks: {}, Waypoints: {}, Routes: {}".format(len(gpx.tracks), len(gpx.waypoints), len(gpx.routes)))


#points = [p for p in s for s in t.segments for t in gpx.tracks]
points = [[seg.points for seg in t.segments] for t in gpx.tracks]

points = []
plt.scatter(-1, -1, c="r")
plt.scatter(-1, -1, c="b")
plt.scatter(-1, -1, c="y")
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            points.append(point)

times = [p.time for p in points]
t_min = min(times)
durations = [(t - t_min).total_seconds() for t in times]
heights = [p.elevation for p in points]
delta_h = np.diff(heights)
delta_h_filt = smooth(np.append(0, delta_h), 7)

delta_t = np.diff(durations)
v_z = delta_h_filt/np.append(0, delta_t)

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
plt.legend(['going up', 'going down', 'not moving'])
plt.savefig('plot.png', dpi=600)
