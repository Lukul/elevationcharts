import matplotlib.pyplot as plt
import matplotlib

class Point:
	def __init__(self, distance, elevation, annotation = '', water = False):
		self.distance = distance
		self.elevation = elevation
		self.annotation = annotation
		self.water = water

def split(a, n):
	k, m = divmod(len(a), n)
	return [a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


def reformat_thousand_to_k(tick_val, pos):
	if tick_val >= 1000:
		val = int(tick_val / 1000)
		new_tick_format = '{:}K'.format(val)
	else:
		new_tick_format = int(tick_val)
	return str(new_tick_format)

def plot_elevation_chart(x_track, y_track, waypoint_indicies, annotations, water, rows=1, pages=6):
	points = [Point(x, y_track[i]) for i, x in enumerate(x_track)]
	for i, index in enumerate(waypoint_indicies):
		points[index].annotation = annotations[i]
		points[index].water = water[i]
	split_points = split(points, rows*pages)
	for i in range(pages):
		plot_single_pdf_page(split_points[i*rows:(i+1)*rows], rows, i)

def plot_single_pdf_page(split_points, rows, page, size=(8.27, 11.69)):
	fig, axs = plt.subplots(rows)
	for i in range(rows):
		x, y, a, w = zip(*[(point.distance, point.elevation, point.annotation, point.water) for point in split_points[i]])
		axs[i].plot(x, y, color='black')
		for j, txt in enumerate(a):
			if txt != '':
				if w[j]:
					axs[i].annotate(txt, (x[j], y[j]), xytext=(7, 25), textcoords='offset points', color='blue', ha='center',
					                va='center', arrowprops=dict(arrowstyle="-", relpos=(0.21,0.4)), rotation=45, size=6)
				else:
					axs[i].annotate(txt, (x[j], y[j]), xytext=(7, -25), textcoords='offset points', color='green', ha='center',
					                va='center', arrowprops=dict(arrowstyle="-", relpos=(0.21,0.6)), rotation=-45, size=6)
		axs[i].set_xlim([min(x), max(x)])
		axs[i].set_ylim([0, round(max(y) + 500, -3)])
		axs[i].grid()
		axs[i].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(reformat_thousand_to_k))

	title = 'PCT Page ' + str(page) + ': Elevation [ft]; Distance [mi]; 1 mi = 1.6 km; 1000 ft = 300 m'
	axs[0].set_title(title)
	fig.set_size_inches(size)
	fig.tight_layout()
	file = 'PCTElevation' + str(page) + '.pdf'
	plt.savefig(file)
	plt.show()