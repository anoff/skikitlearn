import gpxpy
import numpy as np
from collections import namedtuple

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

def calc_additional(points):
    times = [p.time for p in points]
    t_min = min(times)
    duration = [(t - t_min).total_seconds() for t in times]
    height = smooth([p.elevation for p in points], 5)
    d_height = np.append(0, np.diff(height))
    distance = smooth([p.distance for p in points], 5)
    d_distance = np.append(0, np.diff(distance))

    return duration, height, d_height, distance, d_distance
