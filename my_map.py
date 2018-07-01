# module for creating map objects
import folium

# module for working with json and txt files
import pandas

data = pandas.read_csv("Volcanoes_USA.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

# change marker's color depending on elevation
def color_producer(elevation):
	if elevation < 1000:
		return 'green'
	elif 1000 <= elevation < 3000:
		return 'orange'
	else:
		return 'red'

# create map object
map = folium.Map(location=[35.58, -99.09], zoom_start=3, tiles="Mapbox Bright")

# create feature group to accumulate all markers
fgv = folium.FeatureGroup(name="Volcanoes")

# add markers to map using coordinates from Volcanoes_USA.txt file
	# you may get a blank page if there are quotes (') in the strings. To avoid it: popup = folium.Popup(str(el), parse_html=True)
for lt, ln, el in zip(lat, lon, elev):
	fgv.add_child(folium.Marker(location=[lt, ln], popup=str(el), icon=folium.Icon(color=color_producer(el) )))

fgp = folium.FeatureGroup(name="Population")
# add new layer with polygons (states' borders) to featuregroup
fgp.add_child( folium.GeoJson( data = open( 'world.json', 'r', encoding='utf-8-sig' ).read(),
style_function = lambda x: { 'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red' } ) ) 
 
map.add_child(fgp)
map.add_child(fgv)

# add button show/hide layers
map.add_child(folium.LayerControl())

# generate html file with map
map.save('my_map.html')