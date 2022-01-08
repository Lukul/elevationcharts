import gpx_conversion
import chart_plot

if __name__ == '__main__':
	distance, elevation = gpx_conversion.get_distance_and_elevation('data/PacificCrestTrail/CA_Sec_A_tracks.gpx')
	chart_plot.plot_elevation_chart(distance, elevation, 3)

