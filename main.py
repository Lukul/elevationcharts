import gpx_conversion
import chart_plot

if __name__ == '__main__':
	distance = []
	elevation = []

	waypoint_index = []
	annotation = []

	for c in 'A': #BCDEFGHIJKLMNOPQR':
		starting_index = len(distance)
		segment = gpx_conversion.segment('data/PacificCrestTrail/CA_Sec_'+ c + '_tracks.gpx',
		                                 'data/PacificCrestTrail/CA_Sec_' + c + '_waypoints.gpx')
		d, e = segment.get_distance_and_elevation(distance[-1] if len(distance) != 0 else 0)
		distance.extend(d)
		elevation.extend(e)
		wi, a = segment.get_water_and_campsites()
		wi = [index + starting_index for index in wi]
		waypoint_index.extend(wi)
		annotation.extend(a)

	'''
	for c in 'BCDEFG':
		d, e = gpx_conversion.get_distance_and_elevation('data/PacificCrestTrail/OR_Sec_'+ c + '_tracks.gpx',
		                                                 distance[-1] if len(distance) != 0 else 0)
		distance.extend(d)
		elevation.extend(e)
	for c in 'HIJKL':
		d, e = gpx_conversion.get_distance_and_elevation('data/PacificCrestTrail/WA_Sec_'+ c + '_tracks.gpx',
		                                                 distance[-1] if len(distance) != 0 else 0)
		distance.extend(d)
		elevation.extend(e)
	'''

	chart_plot.plot_elevation_chart(distance, elevation, waypoint_index, annotation, 5)

