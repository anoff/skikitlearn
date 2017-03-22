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
print(len(gpx.tracks[0].segments[0].points))
points = []
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            points.append(point)
print(len(points))
times = [p.time for p in points]
t_min = min(times)
durations = [(t - t_min).total_seconds() for t in times]
heights = [p.elevation for p in points]
delta_h = smooth(np.append(0, np.diff(heights)), 7)

print(len(delta_h), len(durations))
#plt.plot(durations, heights, c='b')
#plt.plot(durations, delta_h*100, c='r')
for ix in range(len(durations)):
    if delta_h[ix] > 0:
        c = 'r'
    elif delta_h[ix] == 0:
        c = 'y'
    else:
        c = 'b'
    plt.scatter(durations[ix], heights[ix], c=c)

plt.savefig('plot.png')
