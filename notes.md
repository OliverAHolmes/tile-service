-r <resampling_method>
Resampling method to use. Available methods are:

near: nearest neighbour resampling (default, fastest algorithm, worst interpolation quality).

bilinear: bilinear resampling.

cubic: cubic resampling.

cubicspline: cubic spline resampling.

lanczos: Lanczos windowed sinc resampling.

average: average resampling, computes the weighted average of all non-NODATA contributing pixels.

rms root mean square / quadratic mean of all non-NODATA contributing pixels (GDAL >= 3.3)

mode: mode resampling, selects the value which appears most often of all the sampled points. In the case of ties, the first value identified as the mode will be selected.

max: maximum resampling, selects the maximum value from all non-NODATA contributing pixels.

min: minimum resampling, selects the minimum value from all non-NODATA contributing pixels.

med: median resampling, selects the median value of all non-NODATA contributing pixels.

q1: first quartile resampling, selects the first quartile value of all non-NODATA contributing pixels.

q3: third quartile resampling, selects the third quartile value of all non-NODATA contributing pixels.

sum: compute the weighted sum of all non-NODATA contributing pixels (since GDAL 3.1)




https://jimmyutterstrom.com/blog/2019/06/05/map-tiles-to-geotiff/


https://gis.stackexchange.com/questions/264793/crop-raster-in-memory-with-python-gdal-bindings

source venv/bin/activate
