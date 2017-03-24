import matplotlib.pyplot as plt
from lib.process import load_points, calc_additional, smooth

points = load_points('data/runtastic_20170322_1454_Skiing.gpx')
duration, height, d_height, distance, d_distance = calc_additional(points)

# smooth over wider window to identify larger regions of up/down (lifting)
windowed_height = smooth(d_height, 20)

plt.figure(1)
#http://stackoverflow.com/questions/35372993/python-matplotlib-multicolor-line
for lon1, lon2, lat1, lat2, dh in zip([p.lon for p in points], [p.lon for p in points][1:], [p.lat for p in points], [p.lat for p in points][1:], windowed_height):
    if dh > 0:
        plt.plot([lon1, lon2], [lat1, lat2], 'r')
    elif dh < 0:
        plt.plot([lon1, lon2], [lat1, lat2], 'b')
    else:
        plt.plot([lon1, lon2], [lat1, lat2], 'y')
plt.plot()
plt.ylabel("latitude")
plt.xlabel("longitude")
plt.title("gps track")
plt.savefig('pos.png', dpi=320)
