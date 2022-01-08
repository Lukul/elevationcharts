import gpxpy.gpx
import geopy.distance

def get_distance_and_elevation(filepath):
	gpx_file = open(filepath, 'r')

	gpx = gpxpy.parse(gpx_file)

	distance_from_start = []
	elevation = []

	accumulated_distance = 0
	for segment in gpx.tracks[0].segments:
		for i, point in enumerate(segment.points[:-1]):
			pointA = (segment.points[i].latitude, segment.points[i].longitude)
			pointB = (segment.points[i + 1].latitude, segment.points[i + 1].longitude)
			accumulated_distance += geopy.distance.distance(pointA, pointB).mi
			distance_from_start.append(accumulated_distance)
			elevation.append(geopy.units.feet(meters=segment.points[i].elevation))

	# for waypoint in gpx.waypoints:
	#    print('waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))

	return distance_from_start, elevation
