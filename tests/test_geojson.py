import os
import json
from collections import OrderedDict
import geojson
import mappyfile_geojson
import mappyfile
import pytest


def get_geojson(fn):
    tests = os.path.dirname(os.path.realpath(__file__))

    fn = os.path.join(tests, fn)
    with open(fn) as f:
        gj = geojson.load(f, object_pairs_hook=OrderedDict)

    return gj


def test_point():
    gj = get_geojson("Point.json")
    layer = mappyfile_geojson.convert(gj)
    s = mappyfile.dumps(layer)
    print(s)
    assert s == """LAYER
    EXTENT 102.0 0.5 102.0 0.5
    STATUS ON
    TYPE POINT
    PROCESSING "ITEMS=prop0"
    FEATURE
        POINTS
            102.0 0.5
        END
        ITEMS "value0"
    END
END"""


def test_linestring():
    gj = get_geojson("LineString.json")
    layer = mappyfile_geojson.convert(gj)
    s = mappyfile.dumps(layer)
    print(s)
    assert s == """LAYER
    EXTENT 102.0 0.0 105.0 1.0
    STATUS ON
    TYPE LINE
    PROCESSING "ITEMS=prop0,prop1"
    FEATURE
        POINTS
            102.0 0.0
            103.0 1.0
            104.0 0.0
            105.0 1.0
        END
        ITEMS "value0;0.0"
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
        POINTS
            100.0 0.0
            101.0 0.0
            101.0 1.0
            100.0 1.0
            100.0 0.0
        END
        ITEMS "value0;{u'this': u'that'}"
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
        POINTS
            102.0 0.0
            103.0 1.0
            104.0 0.0
            105.0 1.0
        END
        ITEMS "value0"
    END
    FEATURE
        POINTS
            102.0 0.0
            103.0 1.0
            104.0 0.0
            105.0 1.0
        END
        ITEMS "value1"
    END
END"""


def run_tests():
    pytest.main(["tests/test_geojson.py", "-vv"])


if __name__ == '__main__':
    test_featurecollection()
    test_point()
    test_linestring()
    test_polygon()
    run_tests()
    print("Done!")
