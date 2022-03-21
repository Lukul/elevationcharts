import gpxpy.gpx
import geopy.distance

class segment():
	def __init__(self, track_filepath, waypoints_filepath):
		gpx_file = open(track_filepath, 'r')
		self.track = gpxpy.parse(gpx_file).tracks[0]
		gpx_file = open(waypoints_filepath, 'r')
		self.waypoints = gpxpy.parse(gpx_file).waypoints

	def get_distance_and_elevation(self, accumulated_distance=0):
		self.distance_from_start = []
		elevation = []

		for segment in self.track.segments:
			for i, point in enumerate(segment.points[:-1]):
				pointA = (segment.points[i].latitude, segment.points[i].longitude)
				pointB = (segment.points[i + 1].latitude, segment.points[i + 1].longitude)
				accumulated_distance += geopy.distance.distance(pointA, pointB).mi
				self.distance_from_start.append(accumulated_distance)
				elevation.append(geopy.units.feet(meters=segment.points[i].elevation))

		return self.distance_from_start, elevation

	def get_water_and_campsites(self):
		waypoint_index = []
		annotation = []
		for waypoint in self.waypoints:
			waypoint.
			if waypoint.name[:2] == 'WR' or waypoint.name[:2] == 'CS':
				waypoint_index.append(self.get_distance_from_start(waypoint))
				# Halfmile uses always WR for Water and CS for Campsites
				annotation.append('W' if waypoint.name[:2] == 'WR' else 'C')

		return waypoint_index, annotation

	def get_distance_from_start(self, waypoint):
		distance_to_trackpoints = []
		pointWaypoint = (waypoint.latitude, waypoint.longitude)

		for segment in self.track.segments:
			for i, point in enumerate(segment.points[:-1]):
				pointTrack = (point.latitude, point.longitude)
				distance_to_trackpoints.append(geopy.distance.distance(pointTrack, pointWaypoint).mi)

		val, idx = min((val, idx) for (idx, val) in enumerate(distance_to_trackpoints))

		print(val,idx)

		return idx