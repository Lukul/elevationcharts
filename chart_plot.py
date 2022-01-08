import matplotlib.pyplot as plt

def split(a, n):
	k, m = divmod(len(a), n)
	return [a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

def plot_elevation_chart(x, y, rows=1, size=(11.69, 8.27)):
	split_distance = split(x, rows)
	split_elevation = split(y, rows)

	fig, axs = plt.subplots(rows)
	for i in range(rows):
		axs[i].plot(split_distance[i], split_elevation[i], color='black')

	plt.ylabel('Elevation [ft]')
	plt.xlabel('Distance [mi]')
	fig.set_size_inches(size)
	plt.show()