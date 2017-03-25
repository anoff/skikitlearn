import matplotlib.pyplot as plt
from lib.process import load_points, calc_additional, smooth, extract_rides

points = load_points('data/runtastic_20170322_1454_Skiing.gpx')
duration, height, d_height, distance, d_distance = calc_additional(points)

# smooth over wider window to identify larger regions of up/down (lifting)
windowed_height = smooth(d_height, 20)

rides = extract_rides(points)
plt.figure(1)
#http://stackoverflow.com/questions/35372993/python-matplotlib-multicolor-line
for points in rides:
    duration, height, d_height, distance, d_distance = calc_additional(points)
    plt.plot([p.lon for p in points], [p.lat for p in points])
plt.ylabel("latitude")
plt.xlabel("longitude")
plt.title("gps track")
plt.savefig('pos.png', dpi=320)
