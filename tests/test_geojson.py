import os
import json
import geojson
import mappyfile_geojson
import mappyfile
import pytest


def get_geojson(fn):
    tests = os.path.dirname(os.path.realpath(__file__))

    fn = os.path.join(tests, fn)
    with open(fn) as f:
        gj = geojson.load(f)

    return gj


def test_point():
    gj = get_geojson("Point.json")
    layer = mappyfile_geojson.convert(gj)
    s =mappyfile.dumps(layer)
    assert s == """LAYER
    EXTENT 102.0 0.5 102.0 0.5
    STATUS ON
    TYPE POINT
    PROCESSING "ITEMS=prop0"
    FEATURE
        ITEMS "value0"
        POINTS
            102.0 0.5
        END
    END
END"""


def test_linestring():
    gj = get_geojson("LineString.json")
    layer = mappyfile_geojson.convert(gj)
    s = mappyfile.dumps(layer)
    assert s == """LAYER
    EXTENT 102.0 0.0 105.0 1.0
    STATUS ON
    TYPE LINE
    PROCESSING "ITEMS=prop0,prop1"
    FEATURE
        ITEMS "value0;0.0"
        POINTS
            102.0 0.0
            103.0 1.0
            104.0 0.0
            105.0 1.0
        END
    END
END"""


def test_polygon():
    gj = get_geojson("Polygon.json")
    layer = mappyfile_geojson.convert(gj)
    print(json.dumps(layer, indent=4))
    s = mappyfile.dumps(layer)
    print(s)
    assert s == """LAYER
    EXTENT 100.0 0.0 101.0 1.0
    STATUS ON
    TYPE POLYGON
    PROCESSING "ITEMS=prop0,prop1"
    FEATURE
        ITEMS "value0;{u'this': u'that'}"
        POINTS
            100.0 0.0
            101.0 0.0
            101.0 1.0
            100.0 1.0
            100.0 0.0
        END
    END
END"""


def test_featurecollection():
    gj = get_geojson("FeatureCollection.json")
    layer = mappyfile_geojson.convert(gj)
    print(json.dumps(layer, indent=4))
    s = mappyfile.dumps(layer)
    print(s)
    assert s == """LAYER
    EXTENT 102.0 0.0 105.0 1.0
    STATUS ON
    TYPE LINE
    PROCESSING "ITEMS=prop0"
    FEATURE
        ITEMS "value0"
        POINTS
            102.0 0.0
            103.0 1.0
            104.0 0.0
            105.0 1.0
        END
    END
    FEATURE
        ITEMS "value1"
        POINTS
            102.0 0.0
            103.0 1.0
            104.0 0.0
            105.0 1.0
        END
    END
END"""


def run_tests():
    pytest.main(["tests/test_geojson.py"])


if __name__ == '__main__':
    #test_featurecollection()
    run_tests()
    print("Done!")
