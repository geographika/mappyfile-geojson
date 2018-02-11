import mappyfile
import mappyfile_geojson
import geojson

gj = '''{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [30, 10], [40, 40], [20, 40], [10, 20], [30, 10]
    ]
  }
}'''

# load a string into a GeoJSON object
gj = geojson.loads(gj)

# convert it to a mappyfile layer dict
layer = mappyfile_geojson.convert(gj, extent_buffer=10)

# now load a Mapfile
mf = mappyfile.load("example.map")
# find an existing layer by name
map_layer = mappyfile.find(mf["layers"], "name", "Polygon")
# apply the FEATURES from GeoJSON to the layer
map_layer.update(layer)
# update the map extent to the extent of the features
mf["extent"] = layer["extent"]
# we now have a layer populated from the GeoJSON
s = mappyfile.dumps(mf)
print(s)
