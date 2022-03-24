import gpxpy.gpx
import geopy.distance
import math

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
				distance = geopy.distance.distance(pointA, pointB).meters
				height = segment.points[i].elevation - segment.points[i + 1].elevation
				accumulated_distance += geopy.units.miles(meters=math.sqrt(distance**2 + height**2)) * 1.01878
				self.distance_from_start.append(accumulated_distance)
				elevation.append(geopy.units.feet(meters=segment.points[i].elevation))

		'''
		calculated_distance = self.distance_from_start[-1]
		distance_from_book = 109.5

		normalization_factor = distance_from_book / calculated_distance
		self.distance_from_start = [x * normalization_factor for x in self.distance_from_start]
		'''

		return self.distance_from_start, elevation

	def get_water_and_campsites(self):
		waypoint_index = []
		annotation = []
		water = [] #or camp
		for waypoint in self.waypoints:
			if any(x in waypoint.symbol for x in ['Water Source', 'Campground']):
				distance, index = self.get_distance_from_start(waypoint)
				elevation_deviation = abs(waypoint.elevation - self.track.segments[0].points[index].elevation)
				if distance < 0.5 and elevation_deviation < 50:
					waypoint_index.append(index)
					annotation.append(waypoint.name)
					if waypoint.symbol == 'Water Source':
						water.append(True)
					else:
						water.append(False)
				else:
					print('Left out ', waypoint.name, ' with ', distance,
					      ' miles to the track. Elevation deviation was ', elevation_deviation,' meters')

		return waypoint_index, annotation, water

	def get_distance_from_start(self, waypoint):
		distance_to_trackpoints = []
		pointWaypoint = (waypoint.latitude, waypoint.longitude)

		for segment in self.track.segments:
			for i, point in enumerate(segment.points[:-1]):
				pointTrack = (point.latitude, point.longitude)
				distance_to_trackpoints.append(geopy.distance.distance(pointTrack, pointWaypoint).mi)

		val, idx = min((val, idx) for (idx, val) in enumerate(distance_to_trackpoints))

		return val, idx