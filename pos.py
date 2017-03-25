import matplotlib.pyplot as plt
import os
from lib.process import load_points, calc_additional, smooth, extract_rides

rides = []
for root, dirs, files in os.walk('data/'):
    for f in files:
        pts = load_points(os.path.join(root, f))
        rds = extract_rides(pts)
        for ride in rds:
            rides.append(ride)

plt.figure(1)
#http://stackoverflow.com/questions/35372993/python-matplotlib-multicolor-line
dist = 0
for points in rides:
    duration, height, d_height, distance, d_distance = calc_additional(points)
    plt.plot([p.lon for p in points], [p.lat for p in points])
    #print("distance: {}".format(sum(distance)))
    dist += sum(distance)

print("distance: {}".format(dist/1000))
plt.ylabel("latitude")
plt.xlabel("longitude")
plt.title("gps track")
plt.savefig('pos.png', dpi=320)
