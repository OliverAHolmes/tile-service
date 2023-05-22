from osgeo import gdal, osr

def reproject_dataset( dataset ):

    # Open the input dataset
    input_ds = gdal.Open(dataset)

    # Get the input dataset's SRS
    input_srs = osr.SpatialReference()
    input_srs.ImportFromEPSG ( 7850 )
    # input_srs.ImportFromWkt(input_ds.GetProjection())

    # Define the output SRS
    output_srs = osr.SpatialReference()
    output_srs.ImportFromEPSG ( 3857 )

    # Create a transformation object from input to output SRS
    transform = osr.CoordinateTransformation(input_srs, output_srs)

    # Create the output dataset
    driver = gdal.GetDriverByName('GTiff')
    output_ds = driver.Create('output_1.tif', input_ds.RasterXSize, input_ds.RasterYSize, input_ds.RasterCount, input_ds.GetRasterBand(1).DataType)

    # Set the output dataset's SRS
    output_ds.SetProjection(output_srs.ExportToWkt())

    gdal.ReprojectImage( input_ds, output_ds, \
                input_srs.ExportToWkt(), output_srs.ExportToWkt(), \
                gdal.GRA_Bilinear )

    # # Loop over each band of the input dataset and reproject it to the output SRS
    # for i in range(1, input_ds.RasterCount + 1):
    #     band = input_ds.GetRasterBand(i)
    #     reprojected_band = output_ds.GetRasterBand(i)
    #     gdal.ReprojectImage(band, reprojected_band, input_srs.ExportToWkt(), output_srs.ExportToWkt(), gdal.GRA_Bilinear)

    # Close the input and output datasets
    input_ds = None
    output_ds = None

# def reproject_dataset ( dataset, \
#             pixel_spacing=5000., epsg_from=7850, epsg_to=3857 ):
#     """
#     A sample function to reproject and resample a GDAL dataset from within 
#     Python. The idea here is to reproject from one system to another, as well
#     as to change the pixel size. The procedure is slightly long-winded, but
#     goes like this:
    
#     1. Set up the two Spatial Reference systems.
#     2. Open the original dataset, and get the geotransform
#     3. Calculate bounds of new geotransform by projecting the UL corners 
#     4. Calculate the number of pixels with the new projection & spacing
#     5. Create an in-memory raster dataset
#     6. Perform the projection
#     """
#     # Define the UK OSNG, see <http://spatialreference.org/ref/epsg/27700/>
#     osng = osr.SpatialReference ()
#     osng.ImportFromEPSG ( epsg_to )
#     wgs84 = osr.SpatialReference ()
#     wgs84.ImportFromEPSG ( epsg_from )
#     tx = osr.CoordinateTransformation ( wgs84, osng )
#     # Up to here, all  the projection have been defined, as well as a 
#     # transformation from the from to the  to :)
#     # We now open the dataset
#     g = gdal.Open ( dataset )

#     print (dataset)

#     # Get the Geotransform vector
#     geo_t = g.GetGeoTransform ()
#     x_size = g.RasterXSize # Raster xsize
#     y_size = g.RasterYSize # Raster ysize

#     print (x_size)
#     print (y_size)

#     # Work out the boundaries of the new dataset in the target projection
#     (ulx, uly, ulz ) = tx.TransformPoint( geo_t[0], geo_t[3])

#     print (ulx, uly, ulz)


#     (lrx, lry, lrz ) = tx.TransformPoint( geo_t[0] + geo_t[1]*x_size, \
#                                           geo_t[3] + geo_t[5]*y_size )
    
#     print (lrx, lry, ulz)

#     # See how using 27700 and WGS84 introduces a z-value!
#     # Now, we create an in-memory raster
#     mem_drv = gdal.GetDriverByName( 'MEM' )
#     # The size of the raster is given the new projection and pixel spacing
#     # Using the values we calculated above. Also, setting it to store one band
#     # and to use Float32 data type.

#     print (int((lrx - ulx)/pixel_spacing), int((uly - lry)/pixel_spacing))


#     dest = mem_drv.Create('', int((lrx - ulx)/pixel_spacing), \
#             int((uly - lry)/pixel_spacing), 1, gdal.GDT_Float32)
#     # Calculate the new geotransform
#     new_geo = ( ulx, pixel_spacing, geo_t[2], \
#                 uly, geo_t[4], -pixel_spacing )
#     # Set the geotransform
#     dest.SetGeoTransform( new_geo )
#     dest.SetProjection ( osng.ExportToWkt() )
#     # Perform the projection/resampling 
#     res = gdal.ReprojectImage( g, dest, \
#                 wgs84.ExportToWkt(), osng.ExportToWkt(), \
#                 gdal.GRA_Bilinear )
#     return dest

reproject_dataset ( './datasets/output_trans.tif' )