import folium
import pandas

data = pandas.read_csv("Webmap_datasources\Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_producer(elevation):
    if elevation > 2000:
        return "green"
    else:
        return "blue"

map = folium.Map(location=[38, -100], zoom_start=6, tiles="Stamen Terrain")

#adds Marker 
fgVolcanoes = folium.FeatureGroup(name="Volcanoes")
for lati,lonti,ele,name in zip(lat,lon,elev,name):
    iframe = folium.IFrame(html=html % (name, name, ele), width=200, height=100)
    fgVolcanoes.add_child(folium.Marker(location=[lati,lonti],popup=folium.Popup(iframe), icon=folium.Icon(color=color_producer(ele))))

#adds GeoJson
fgBoundary = folium.FeatureGroup(name="Boundary and Population")
fgBoundary.add_child(folium.GeoJson(data=(open('Webmap_datasources\world.json', 'r', encoding='utf-8-sig').read()), 
style_function= lambda x: {'fillColor' : 'green' if x['properties']['POP2005'] < 10000000
else 'red' if 10000000 < x['properties']['POP2005'] < 20000000 else 'orange'}))

#generates map
map.add_child(fgVolcanoes)
map.add_child(fgBoundary)
map.add_child(folium.LayerControl())
map.save("Map1.html") 