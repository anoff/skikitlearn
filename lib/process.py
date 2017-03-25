import gpxpy
import numpy as np
from collections import namedtuple

def smooth(y, box_pts=11):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

# load file and concat all tracks/segments
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

# generate additional values
def calc_additional(points):
  times = [p.time for p in points]
  t_min = min(times)
  duration = [(t - t_min).total_seconds() for t in times]
  height = smooth([p.elevation for p in points], 5)
  d_height = np.append(0, np.diff(height))
  distance = smooth([p.distance for p in points], 5)
  d_distance = np.append(0, np.diff(distance))

  return duration, height, d_height, distance, d_distance

# extract rides
# consecutive points with decreasing elevation & no stops (change in elevation) > 60s
def extract_rides(points):
    duration, height, d_height, distance, d_distance = calc_additional(points)
    smooth_d_height = smooth(d_height, 20)
    indices = []
    index = {"start": 0, "end": 0}
    for ix in range(len(points)):
        if smooth_d_height[ix] < 0 and (ix == 0 or smooth_d_height[ix-1] > 0):
            index["start"] = ix
        elif index["start"] > 0 and smooth_d_height[ix] > 0:
            index["end"] = ix
            print(index)
            indices.append(index)
            index = {"start": 0, "end": 0}
    rides = []
    for trk in indices:
      rides.append(points[trk["start"]:trk["end"]])
    return rides
