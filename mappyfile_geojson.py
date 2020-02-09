import sys
from collections import OrderedDict

__version__ = "0.4.0"


# for Python3 long is no longer used
PY2 = sys.version_info[0] < 3
if not PY2:
    long = int # NOQA
    unicode = str # NOQA


def explode(coords):
    """
    From https://gist.github.com/sgillies/3975665
    Explode a GeoJSON geometry's coordinates object and yield
    coordinate tuples. As long as the input is conforming,
    the type of the geometry doesn't matter.
    """

    for e in coords:
        if isinstance(e, (float, int, long)):
            yield coords[:2]  # strip out any Z values from the coords
            break
        else:
            for f in explode(e):
                yield f


def bbox(f):
    x, y = zip(*list(explode(f.geometry.coordinates)))
    return min(x), min(y), max(x), max(y)


def get_extent(features, buffer=0):

    extents = [bbox(f) for f in features]
    all_extents = list(zip(*extents))

    full_extent = (min(all_extents[0]) - buffer,
                   min(all_extents[1]) - buffer,
                   max(all_extents[2]) + buffer,
                   max(all_extents[3]) + buffer)

    # use integers if floats have no precision e.g. use 5 for 5.0
    full_extent = (int(c) if isinstance(c, float) and c.is_integer() else c for c in full_extent)

    return list(full_extent)


def create_inline_feature(feat, props):

    geom = feat.geometry
    f = OrderedDict()
    f["__type__"] = "feature"

    coords = geom.coordinates

    if geom.type == "Point":
        coords = [coords]  # put coords in an outer list
    elif geom.type == "MultiPolygon":
        coords = [c[0] for c in coords]  # remove one layer of list nesting

    f["points"] = coords
    # note items use semicolons and not commas as used elsewhere
    values = [unicode(feat.properties[p]) for p in props]
    f["items"] = ";".join(values)
    return f


def get_features(gj):

    if gj.type == "FeatureCollection":
        features = gj.features
    elif gj.type == "Feature":
        features = [gj]

    return features


def create_layer(features, bbox):

    first_feature = features[0]
    # properties will be an unsorted dict, so
    # sort to ensure consistency
    props = sorted(first_feature.properties.keys())
    geom_type = first_feature.geometry.type

    mapfile_features = [create_inline_feature(f, props) for f in features]

    layer = OrderedDict()
    layer["__type__"] = "layer"
    layer["extent"] = bbox
    layer["status"] = "on"

    if geom_type in ("LineString", "MultiLineString"):
        layer_type = "line"
    elif geom_type in ("Point", "MultiPoint"):
        layer_type = "point"
    elif geom_type in ("Polygon", "MultiPolygon"):
        layer_type = "polygon"
    else:
        msg = "The geometry type {} is not yet implemented".format(geom_type)
        raise NotImplementedError(msg)

    # layer type must be set before adding inline features!!

    layer["type"] = layer_type
    layer["processing"] = ["ITEMS={}".format(",".join(props))]
    layer["features"] = mapfile_features
    return layer


def convert(gj, extent_buffer=0):
    features = get_features(gj)
    bbox = get_extent(features, buffer=extent_buffer)
    layer = create_layer(features, bbox)
    return layer
