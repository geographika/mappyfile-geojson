"""
In order to generate image output mapscript needs to be installed.
On Windows this can be run using:

pip install mapscript

Make sure that MapServer is also on the system path before running the script e.g. (on Windows):

SET PATH=C:/MapServer/bin;%PATH%
cd /D /mappyfile-geojson
python create_images.py

"""

import os
import geojson
import mappyfile_geojson
import mappyfile
import glob
import mapscript


def get_geojson(fn):
    tests = os.path.dirname(os.path.realpath(__file__))

    fn = os.path.join(tests, fn)
    with open(fn) as f:
        gj = geojson.load(f)

    return gj


def create_image(f):
    basename = os.path.splitext(os.path.basename(f))[0] + ".png"
    fn = os.path.join("tests", "images", basename)
    print("Creating {}".format(fn))

    # create the new layer
    gj = get_geojson(f)
    layer = mappyfile_geojson.convert(gj, extent_buffer=5)

    # open the example map
    m = mappyfile.open("example.map")
    m["extent"] = layer["extent"]  # set the map extent to the layer extent
    poly_layer = m["layers"][0]  # turn of the sample layer
    poly_layer["status"] = "off"

    layer["classes"] = poly_layer[
        "classes"
    ]  # take the existing symbology from the sample layer
    m["layers"].insert(0, layer)  # add the GeoJSON layer to the map

    # print(mappyfile.dumps(m))

    # now open the Mapfile with Mapscript and create an image
    mo = mapscript.fromstring(mappyfile.dumps(m))
    img = mo.draw()
    img.save(fn)


def main():
    jsn_files = glob.glob("tests/*.json")
    for f in jsn_files:
        create_image(f)


main()
print("Done!")
