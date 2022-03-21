import gpx_conversion
import chart_plot
import pickle

def tracks_and_waypoints(distance, elevation, waypoint_index, annotation, tracks, waypoints):
	print(tracks)
	starting_index = len(distance)
	segment = gpx_conversion.segment(tracks, waypoints)
	d, e = segment.get_distance_and_elevation(distance[-1] if len(distance) != 0 else 0)
	distance.extend(d)
	elevation.extend(e)
	wi, a = segment.get_water_and_campsites()
	wi = [index + starting_index for index in wi]
	waypoint_index.extend(wi)
	annotation.extend(a)

def prepare_for_plotting(distance, elevation, waypoint_index, annotation):
	for c in 'ABCDEFGHIJKLMNOPQR':
		tracks_and_waypoints(distance, elevation, waypoint_index, annotation,
		                     'data/PacificCrestTrail/CA_Sec_' + c + '_tracks.gpx',
		                     'data/PacificCrestTrail/CA_Sec_' + c + '_waypoints.gpx')
	for c in 'BCDEFG':
		tracks_and_waypoints(distance, elevation, waypoint_index, annotation,
		                     'data/PacificCrestTrail/OR_Sec_' + c + '_tracks.gpx',
		                     'data/PacificCrestTrail/OR_Sec_' + c + '_waypoints.gpx')
	for c in 'HIJKL':
		tracks_and_waypoints(distance, elevation, waypoint_index, annotation,
		                     'data/PacificCrestTrail/WA_Sec_' + c + '_tracks.gpx',
		                     'data/PacificCrestTrail/WA_Sec_' + c + '_waypoints.gpx')

if __name__ == '__main__':
	distance = []
	elevation = []

	waypoint_index = []
	annotation = []

	recalculate = True

	if not recalculate:
		#distance, elevation, waypoint_index, annotation
		try:
			with open('distance.pkl', 'rb') as f:
				distance = pickle.load(f)
			with open('elevation.pkl', 'rb') as f:
				elevation = pickle.load(f)
			with open('waypoint_index.pkl', 'rb') as f:
				waypoint_index = pickle.load(f)
			with open('annotation.pkl', 'rb') as f:
				annotation = pickle.load(f)
		except FileNotFoundError:
			prepare_for_plotting(distance, elevation, waypoint_index, annotation)

	else:
		prepare_for_plotting(distance, elevation, waypoint_index, annotation)

	with open('distance.pkl', 'wb') as f:
		pickle.dump(distance, f)
	with open('elevation.pkl', 'wb') as f:
		pickle.dump(elevation, f)
	with open('waypoint_index.pkl', 'wb') as f:
		pickle.dump(waypoint_index, f)
	with open('annotation.pkl', 'wb') as f:
		pickle.dump(annotation, f)

	chart_plot.plot_elevation_chart(distance, elevation, waypoint_index, annotation, 5)

