mappyfile-geojson
===================

A mappyfile plugin to convert GeoJSON to inline Mapfile features

Convert to:

LAYER
    FEATURE
        WKT "LINESTRING((50 50, 35 50, 35 25, 50 25, 50 50)"
        ITEMS "809147;0;749.5285764507033"
        TEXT "Hello"
    END
    PROCESSING "ITEMS=edgeId,measureFrom,measureTo" 
END

in JSON:

{
    "__type__": "layer", 
    "features": [
        {
            "__type__": "feature", 
            "wkt": "LINESTRING((500 500, 3500 500, 3500 2500, 500 2500, 500 500)", 
            "items": "809147;0;749.5285764507033"
        }
    ], 
    "processing": [
        "ITEMS=edgeId,measureFrom,measureTo"
    ]
}


