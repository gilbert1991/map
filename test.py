import http_handler as hh
import my_util as mt
import matplotlib.pyplot as plt

interval = 0.0001
path = [(40.694051, -73.983359), (40.690187, -73.981525)]
road = hh.parseJsonRoad(hh.snapToRoad(path))

mt.interpolate(road, interval)
mt.filterPath(road, interval)

print road


marker_style = dict(color='cornflowerblue', linestyle=':', marker='o', 
			markersize=8, markerfacecoloralt='gray')
fig, ax = plt.subplots()
x = []
y = []
for r in road:
	x.append(r[1])
	y.append(r[0])		
	ax.plot(x, y, fillstyle='full', **marker_style)
plt.show()