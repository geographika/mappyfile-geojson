mappyfile-geojson
=================

| |Version| |Build Status|

A `mappyfile <http://mappyfile.readthedocs.io>`_ plugin to convert GeoJSON to 
inline `Mapfile features <http://mapserver.org/mapfile/feature.html>`_. Useful for adding 
dynamically created features (from web services, user created features, and other external
data sources) to a map, or to quickly visualise a geometry. 

Note - to display entire GeoJSON files MapServer
can be configured to read GeoJSON as an input `OGR source <https://mapserver.org/input/vector/ogr.html>`_
using the `GeoJSON driver <https://www.gdal.org/drv_geojson.html>`_. 

.. code-block:: python

    import geojson
    import mappyfile
    # import directly
    import mappyfile_geojson 
    # can also be imported as plugin using
    from mappyfile.plugins import mappyfile_geojson

    gj = geojson.load(fn)
    l = mappyfile_geojson.convert(gj)
    print(mappyfile.dumps(l))

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

.. code-block:: console

    LAYER
        EXTENT 102 0 105 1
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

An example of using the plugin with ``mappyfile`` 
can be found in `example.py <https://github.com/geographika/mappyfile-geojson/blob/master/example.py>`_
along with an `example.map <https://github.com/geographika/mappyfile-geojson/blob/master/example.map>`_. 

.. image:: https://raw.githubusercontent.com/geographika/mappyfile-geojson/master/polygon.png

A further example, creating images for each of the test cases using  `mapscript <https://pypi.org/project/mapscript/>`_ 
is available at `create_images.py <https://github.com/geographika/mappyfile-geojson/blob/master/create_images.py>`_. 

The sample output images are in the `images <https://github.com/geographika/mappyfile-geojson/blob/master/tests/images/>`_
folder. 

Requirements
------------

* Python 2.7 or Python 3.x
* mappyfile (the plugin can be used on its own but will create a dictionary object
  structured to use within mappyfile). Installing mappyfile should be done separately. 

Installation
------------

Note installing the ``mappyfile-geojson`` plugin will automatically install the required dependency ``geojson``. 

.. code-block:: console

    pip install mappyfile
    pip install mappyfile-geojson

Notes
-----

+ Can calculate extent of input features, with an optional buffer (by passing an ``extent_buffer`` to the ``convert``
  function)
+ Multipart features are supported
+ Coordinate sequences with Z values are supported, but Z values are ignored as they are not supported in
  Mapserver inline features. 
+ As a MapServer ``LAYER`` only supports a single geometry type, all features in the GeoJSON file should also
  be of the same type (however a mix of multipart and non-multipart features is supported e.g. LineString and MultiLineString)
+ Nested JSON properties are not supported: 

  .. code-block:: json
  
      "properties": {
          "prop0": "value0",
          "prop1": { "this": "that" }
      }
  
  Will become:
  
  .. code-block:: console
  
      ITEMS "value0;{u'this': u'that'}"

Releases
--------

0.4 (09/02/2020)
++++++++++++++++

+ Automated Windows testing
+ Automated release process
+ Set ``geojson`` dependency version
+ Fix failing tests due to precision issuee differences between py2 and py3
+ Use integers for layer ``EXTENT`` where possible e.g. 5 instead of 5.0

0.3 (29/08/2018)
++++++++++++++++

+ Add support for MultiPoint, MultiLineString, and MultiPolygon
+ Allow coordinates with Z values (previously these would crash the script)
+ Updated README

0.2 (15/02/2018)
++++++++++++++++

+ Unicode support

0.1 (06/02/2018)
++++++++++++++++

+ Initial release

Author
------

* Seth Girvin `@geographika <https://github.com/geographika>`_

.. |Version| image:: https://img.shields.io/pypi/v/mappyfile-geojson.svg
   :target: https://pypi.python.org/pypi/mappyfile-geojson

.. |Build Status| image:: https://travis-ci.org/geographika/mappyfile-geojson.svg?branch=master
   :target: https://travis-ci.org/geographika/mappyfile-geojson
