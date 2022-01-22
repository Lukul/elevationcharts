import matplotlib.pyplot as plt

class Point:
	def __init__(self, distance, elevation, annotation = ''):
		self.distance = distance
		self.elevation = elevation
		self.annotation = annotation

def split(a, n):
	k, m = divmod(len(a), n)
	return [a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

def plot_elevation_chart(x_track, y_track, waypoint_indicies, annotations, rows=1, size=(8.27, 11.69)):
	points = [Point(x, y_track[i]) for i, x in enumerate(x_track)]
	for i, index in enumerate(waypoint_indicies):
		points[index].annotation = annotations[i]
	split_points = split(points, rows)

	fig, axs = plt.subplots(rows)
	for i in range(rows):
		x, y, a = zip(*[(point.distance, point.elevation, point.annotation) for point in split_points[i]])
		axs[i].plot(x, y, color='black')
		for j, txt in enumerate(a):
			if txt == 'W':
				axs[i].annotate(txt, (x[j], y[j]), xytext=(0, 15), textcoords='offset points', color='blue', ha='center',
				                va='center', arrowprops=dict(arrowstyle="-"))
			if txt == 'C':
				axs[i].annotate(txt, (x[j], y[j]), xytext=(0, -15), textcoords='offset points', color='green', ha='center',
				                va='center', arrowprops=dict(arrowstyle="-"))
		axs[i].set_xlim([min(x), max(x)])
		axs[i].set_ylim([0, round(max(y) + 500, -3)])
		axs[i].grid()

	#fig.set_title('1 mi = 1.6 km; 1000 ft = 300 m')
	plt.ylabel('Elevation [ft]')
	plt.xlabel('Distance [mi]')
	fig.set_size_inches(size)
	fig.tight_layout()
	plt.savefig('test.pdf')
	plt.show()