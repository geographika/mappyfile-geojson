mappyfile-geojson
=================

| |Version| |Build Status|

A `mappyfile <http://mappyfile.readthedocs.io>`_ plugin to convert GeoJSON to 
inline `Mapfile features <http://mapserver.org/mapfile/feature.html>`_. Useful for adding 
dynamically created features (from web services, user created features), to a map. 

.. code-block:: python

    import mappyfile_geojson

    gj = geojson.loads(s)
    mappyfile_geojson.convert(gj)

Converts:

.. code-block:: json

    {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [ 102.0, 0.0 ],
          [ 103.0, 1.0 ],
          [ 104.0, 0.0 ],
          [ 105.0, 1.0 ]
        ]
      },
      "properties": {
        "prop0": "value0",
        "prop1": 0.0
      }
    }

to:

.. code-block:: mapfile

    LAYER
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
    END

Demo
----

See the example of using the plugin with ``mappyfile`` 
in `example.py <https://github.com/geographika/mappyfile-geojson/example.py>`_. 

.. image:: https://raw.githubusercontent.com/geographika/mappyfile-geojson/master/polygon.png

Installation
------------

.. code-block:: console

    pip install mappyfile-geojson

Notes
-----

+ Can calculate extent of input features, with optional buffer
+ Multipart features currently not implemented
+ Nested properties are not supported

  .. code-block:: json
  
      "properties": {
          "prop0": "value0",
          "prop1": { "this": "that" }
      }
  
  Will become:
  
  .. code-block:: mapfile
  
      ITEMS "value0;{u'this': u'that'}"

Author
------

* Seth Girvin `@geographika <https://github.com/geographika>`_

.. |Version| image:: https://img.shields.io/pypi/v/mappyfile-geojson.svg
   :target: https://pypi.python.org/pypi/mappyfile-geojson

.. |Build Status| image:: https://travis-ci.org/geographika/mappyfile-geojson.svg?branch=master
   :target: https://travis-ci.org/geographika/mappyfile-geojson
