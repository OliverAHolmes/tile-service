from osgeo import gdal
from PIL import Image
import io
import numpy as np
import math

from math import log, tan, radians, cos, pi, floor, degrees, atan, sinh
from flask import Flask, request, Response
import time
import pyproj
import json

from math import log, tan, radians, cos, pi, floor, degrees, atan, sinh



# def sec(x):
#     return(1/cos(x))


# def latlon_to_xyz(lat, lon, z):
#     tile_count = pow(2, z)
#     x = (lon + 180) / 360
#     y = (1 - log(tan(radians(lat)) + sec(radians(lat))) / pi) / 2
#     return(tile_count*x, tile_count*y)


# def bbox_to_xyz(lon_min, lon_max, lat_min, lat_max, z):
#     x_min, y_max = latlon_to_xyz(lat_min, lon_min, z)
#     x_max, y_min = latlon_to_xyz(lat_max, lon_max, z)
#     return(floor(x_min), floor(x_max), floor(y_min), floor(y_max))


# def mercatorToLat(mercatorY):
#     return(degrees(atan(sinh(mercatorY))))


# def y_to_lat_edges(y, z):
#     tile_count = pow(2, z)
#     unit = 1 / tile_count
#     relative_y1 = y * unit
#     relative_y2 = relative_y1 + unit
#     lat1 = mercatorToLat(pi * (1 - 2 * relative_y1))
#     lat2 = mercatorToLat(pi * (1 - 2 * relative_y2))
#     return(lat1, lat2)


# def x_to_lon_edges(x, z):
#     tile_count = pow(2, z)
#     unit = 360 / tile_count
#     lon1 = -180 + x * unit
#     lon2 = lon1 + unit
#     return(lon1, lon2)


# def tile_edges(x, y, z):
#     lat1, lat2 = y_to_lat_edges(y, z)
#     lon1, lon2 = x_to_lon_edges(x, z)
#     return[lon1, lat1, lon2, lat2]


# start_time = time.time()

# def tile2lon(x, z):
#     return x / pow(2.0, z) * 360.0 - 180

# def tile2lat(y, z):
#     n = math.pi - (2.0 * math.pi * y) / pow(2.0, z)
#     return math.degrees(math.atan(math.sinh(n)))

# def tileToBbox(x, y, zoom):
#     bb = {
#         'north': '',
#         'south': '',
#         'east': '',
#         'west': ''
#     }

#     bb['north'] = tile2lat(y, zoom)
#     bb['south'] = tile2lat(y + 1, zoom)
#     bb['west'] = tile2lon(x, zoom)
#     bb['east'] = tile2lon(x + 1, zoom)

#     polygon = str(bb['west']) + ' ' + str(bb['north']) + ','
#     polygon = polygon + str(bb['east']) + ' ' + str(bb['north']) + ','
#     polygon = polygon + str(bb['east']) + ' ' + str(bb['south']) + ','
#     polygon = polygon + str(bb['west']) + ' ' + str(bb['south']) + ','
#     polygon = polygon + str(bb['west']) + ' ' + str(bb['north'])

#     return polygon

# def pyproj_reproject(coord):
#     proj_to = pyproj.Proj("+proj=longlat +ellps=GRS80 +towgs84=0.06155,-0.01087,-0.04019,0.0394924,0.0327221,0.03289790,-0.009994")
#     lon, lat = proj_to(coord[0], coord[1], inverse=True)
#     return [lon, lat]

# open_file = gdal.Open('output_cog_test.tif', gdal.GA_ReadOnly)

# #create Memory driver
# format = " MEM "
# driver = gdal.GetDriverByName( format )

# #copy data from PostGIS to Memory
# file_in_mem = driver.CreateCopy('', open_file ) 



def sec(x):
    return(1/cos(x))


def latlon_to_xyz(lat, lon, z):
    tile_count = pow(2, z)
    x = (lon + 180) / 360
    y = (1 - log(tan(radians(lat)) + sec(radians(lat))) / pi) / 2
    return(tile_count*x, tile_count*y)


def bbox_to_xyz(lon_min, lon_max, lat_min, lat_max, z):
    x_min, y_max = latlon_to_xyz(lat_min, lon_min, z)
    x_max, y_min = latlon_to_xyz(lat_max, lon_max, z)
    return(floor(x_min), floor(x_max),
           floor(y_min), floor(y_max))


def mercatorToLat(mercatorY):
    return(degrees(atan(sinh(mercatorY))))


def y_to_lat_edges(y, z):
    tile_count = pow(2, z)
    unit = 1 / tile_count
    relative_y1 = y * unit
    relative_y2 = relative_y1 + unit
    lat1 = mercatorToLat(pi * (1 - 2 * relative_y1))
    lat2 = mercatorToLat(pi * (1 - 2 * relative_y2))
    return(lat1, lat2)


def x_to_lon_edges(x, z):
    tile_count = pow(2, z)
    unit = 360 / tile_count
    lon1 = -180 + x * unit
    lon2 = lon1 + unit
    return(lon1, lon2)


def tile_edges(x, y, z):
    lat1, lat2 = y_to_lat_edges(y, z)
    lon1, lon2 = x_to_lon_edges(x, z)
    return[str(lon1), str(lat2), str(lon2), str(lat1)]

def make_tile(layer_name, x, y, z):

    open_file = gdal.Open(layer_name, gdal.GA_ReadOnly)

    start_time_tile = time.time()

    # path = '/vsis3/metromap-ecw-data/' + layer_name
    # ds = gdal.Open(path, gdal.GA_ReadOnly)

    test_mem = '/vsimem/{}_{}_{}.png'.format(x,y,z)
    # tile_bounds = pyproj_reproject(tileToBbox(x,y,z).split(',')[3].split( ' '))
    # tile_bounds.extend(pyproj_reproject(tileToBbox(x,y,z).split(',')[1].split( ' ')))

    print(tile_edges(x,y,z))

    tile_bounds = tile_edges(x,y,z)
    # tile_bounds.extend(tile_edges(x,y,z).split(',')[1].split( ' '))

    print(float(tile_bounds[0]))

    try:
        print(float(tile_bounds[0]))
    except Exception as e:
        print(e)

    

    # # Define the input and output file paths
    # input_file = 'input.tif'
    # output_file = 'output.tif'

    # # Define the cutline as a GeoJSON feature
    # cutline_feature = {
    #     'type': 'Feature',
    #     'properties': {},
    #     'geometry': {
    #         'type': 'Polygon',
    #         'coordinates': [[
    #             [-74.00745391845703, 40.72598765233863],
    #             [-73.9985466003418, 40.72598765233863],
    #             [-73.9985466003418, 40.73176309545619],
    #             [-74.00745391845703, 40.73176309545619],
    #             [-74.00745391845703, 40.72598765233863]
    #         ]]
    #     }
    # }

    # # Define the output raster size and resolution
    # output_size = [256, 256]
    # output_resolution = [0.01, -0.01]  # (X, Y) pixel sizes in CRS units

    # # Define the output raster spatial reference system (CRS)
    # output_crs = 'EPSG:4326'

    # # Convert the cutline feature to a GeoJSON string
    # cutline_geojson = str(cutline_feature)

    # # Define the warp options
    # warp_options = gdal.WarpOptions(
    #     format='GTiff',
    #     cutlineDSName='/vsimem/cutline.geojson',
    #     cropToCutline=True,
    #     cutlineLayer='cutline',
    #     xRes=output_resolution[0],
    #     yRes=output_resolution[1],
    #     dstSRS=output_crs,
    #     width=output_size[0],
    #     height=output_size[1],
    # )

    # # Create a virtual file for the cutline GeoJSON string
    # gdal.FileFromMemBuffer('/vsimem/cutline.geojson', cutline_geojson)

    # # Perform the warp operation
    # gdal.Warp(output_file, input_file, options=warp_options)

    # # Delete the virtual file for the cutline GeoJSON
    # gdal.Unlink('/vsimem/cutline.geojson')

    # # Define the input and output CRS
    # in_crs = 'EPSG:4326'  # WGS84 geographic coordinates
    # out_crs = 'EPSG:7850'  # EPSG code for the new coordinate system
    # transformer = pyproj.Transformer.from_crs(in_crs, out_crs)

    # in_coord = (tile_bounds[1],tile_bounds[0])
    # out_coord = transformer.transform(*in_coord)

    # tile_bounds[0] = out_coord[0]
    # tile_bounds[1] = out_coord[1]

    # in_coord = (tile_bounds[3],tile_bounds[2])
    # out_coord = transformer.transform(*in_coord)

    # tile_bounds[2] = out_coord[0]
    # tile_bounds[3] = out_coord[1]

    # # Define the input coordinate as a tuple of (longitude, latitude)
    # in_coord = (-32.81461011,115.90444134)

    # # Create a PyProj transformer object
    # transformer = pyproj.Transformer.from_crs(in_crs, out_crs)

    # # Reproject the input coordinate
    # out_coord = transformer.transform(*in_coord)

    # print(out_coord)  # Output: (281794.778737951, 348799.0428624712)

    # print(tile_bounds[0],tile_bounds[1],tile_bounds[2],tile_bounds[3])


    # out_ds = gdal.Warp(test_mem, open_file, format='GTiff', outputBounds=[ tile_bounds[0],tile_bounds[1],tile_bounds[2],tile_bounds[3] ],width=256, height=256, dstSRS="EPSG:4326", resampleAlg="bilinear", options=['COMPRESS=DEFLATE'])
    # Resampling method (average, near, bilinear, cubic, cubicspline, lanczos, antialias, mode, max, min, med, q1, q3) - default ‘average’.
    
    
    
    

    try:
        out_ds = gdal.Warp(test_mem, open_file, format='PNG', outputBounds=[ tile_bounds[0],tile_bounds[1],tile_bounds[2],tile_bounds[3] ],errorThreshold=0,width=256, height=256, dstSRS="EPSG:4326", resampleAlg="average")
    
    
        # cutline_feature = {
        #     'type': 'Feature',
        #     'properties': {},
        #     'geometry': {
        #         'type': 'Polygon',
        #         'coordinates': [[
        #             [float(tile_bounds[0]), float(tile_bounds[1])],
        #             [float(tile_bounds[2]), float(tile_bounds[1])],
        #             [float(tile_bounds[2]), float(tile_bounds[3])],
        #             [float(tile_bounds[0]), float(tile_bounds[3])],
        #             [float(tile_bounds[0]), float(tile_bounds[1])]
        #         ]]
        #     }
        # }


        # cutline_geojson = json.dumps(cutline_feature)

        # # Create a virtual file for the cutline GeoJSON string
        # gdal.FileFromMemBuffer('/vsimem/{}_{}_{}.geojson'.format(x,y,z), cutline_geojson)

        # print(cutline_geojson)

        # # Define the output raster spatial reference system (CRS)
        # output_crs = 'EPSG:4326'

        # # Convert the cutline feature to a GeoJSON string
        # cutline_geojson = str(cutline_feature)

        # # Define the warp options
        # warp_options = gdal.WarpOptions(
        #     format='GTiff',
        #     cutlineDSName='/vsimem/{}_{}_{}.geojson'.format(x,y,z),
        #     cropToCutline=True,
        #     cutlineLayer='{}_{}_{}'.format(x,y,z),
        #     dstSRS=output_crs,
        #     width=256,
        #     height=256,
        #     resampleAlg=gdal.GRA_NearestNeighbour
        # )

        # # Perform the warp operation
        # out_ds = gdal.Warp(test_mem, open_file, options=warp_options)

        # # Delete the virtual file for the cutline GeoJSON
        # gdal.Unlink('/vsimem/{}_{}_{}.geojson'.format(x,y,z))
        
        
        # data_1 = out_ds.GetRasterBand(1).ReadRaster(0, 0, 256, 256, buf_type = gdal.GDT_Byte)
        # data_2 = out_ds.GetRasterBand(2).ReadRaster(0, 0, 256, 256, buf_type = gdal.GDT_Byte)
        # data_3 = out_ds.GetRasterBand(3).ReadRaster(0, 0, 256, 256, buf_type = gdal.GDT_Byte)
        # data_4 = out_ds.GetRasterBand(4).ReadRaster(0, 0, 256, 256, buf_type = gdal.GDT_Byte)
        # buf_1 = np.frombuffer(data_1, dtype=np.uint8).reshape((256,256))
        # buf_2 = np.frombuffer(data_2, dtype=np.uint8).reshape((256,256))
        # buf_3 = np.frombuffer(data_3, dtype=np.uint8).reshape((256,256))
        # buf_4 = np.frombuffer(data_4, dtype=np.uint8).reshape((256,256))
        # # Create the RGB array
        # buf_rgb = np.stack((buf_1, buf_2, buf_3, buf_4), axis=-1)

        red_band = out_ds.GetRasterBand(1).ReadAsArray()
        green_band = out_ds.GetRasterBand(2).ReadAsArray()
        blue_band = out_ds.GetRasterBand(3).ReadAsArray()

        # Create an alpha channel array with the desired transparency
        alpha_channel = np.ones_like(red_band, dtype=np.uint8) * 255  # Fully opaque

        # Check if any of the RGB bands have no data
        no_data_mask = (red_band == 0) & (green_band == 0) & (blue_band == 0)

        # Update the alpha channel based on the no data mask
        alpha_channel[no_data_mask] = 0  # Set alpha to 0 for pixels with no data in RGB bands

        # Create the RGBA array by stacking the RGB bands with the updated alpha channel
        rgba_array = np.dstack((red_band, green_band, blue_band, alpha_channel))

        # # Create a new output dataset and write the RGBA array to the appropriate bands
        # driver = gdal.GetDriverByName('GTiff')
        # output_dataset = driver.Create(test_mem1, out_ds.RasterXSize, out_ds.RasterYSize, 4, gdal.GDT_Byte)
        # for i in range(1, 5):  # 4 bands: red, green, blue, alpha
        #     output_dataset.GetRasterBand(i).WriteArray(rgba_array[:, :, i - 1])

        

        # # # Create an RGBA array by stacking the RGB bands with the alpha channel
        # # buf_rgb = np.dstack((red_band, green_band, blue_band, alpha_channel))
        # # driver = gdal.GetDriverByName('GTiff')
        # # output_dataset = driver.Create(test_mem1, out_ds.RasterXSize, out_ds.RasterYSize, 4, gdal.GDT_Byte)
        # # for i in range(1, 5):  # 4 bands: red, green, blue, alpha
        # #     output_dataset.GetRasterBand(i).WriteArray(buf_rgb[:, :, i - 1])

        # data_1 = output_dataset.GetRasterBand(1).ReadRaster(0, 0, 256, 256, buf_type = gdal.GDT_Byte)
        # data_2 = output_dataset.GetRasterBand(2).ReadRaster(0, 0, 256, 256, buf_type = gdal.GDT_Byte)
        # data_3 = output_dataset.GetRasterBand(3).ReadRaster(0, 0, 256, 256, buf_type = gdal.GDT_Byte)
        # data_4 = output_dataset.GetRasterBand(4).ReadRaster(0, 0, 256, 256, buf_type = gdal.GDT_Byte)
        # buf_1 = np.frombuffer(data_1, dtype=np.uint8).reshape((256,256))
        # buf_2 = np.frombuffer(data_2, dtype=np.uint8).reshape((256,256))
        # buf_3 = np.frombuffer(data_3, dtype=np.uint8).reshape((256,256))
        # buf_4 = np.frombuffer(data_4, dtype=np.uint8).reshape((256,256))
        # buf_rgb = np.stack((buf_1, buf_2, buf_3, buf_4), axis=-1)

        # # Define the shape of the RGB array
        # height, width, _ = buf_rgb.shape

        # # Create an alpha channel with the same shape as the RGB array
        # alpha_channel = np.ones((height, width, 1), dtype=np.uint8) * 255  # Set alpha to fully opaque

        # # Concatenate the RGB array and the alpha channel along the last axis
        # buf_rgba = np.concatenate((buf_rgb, alpha_channel), axis=-1)

        return_image = Image.fromarray(rgba_array)

        # data = output_dataset.ReadAsArray()

        # # Transpose the array so that the bands are the last axis
        # data = np.transpose(data, (1, 2, 0))

        # Create a PIL Image object from the NumPy array
        # return_image = Image.fromarray(data, mode='RGBA')

    except Exception as e:
        print(e)

    if return_image.mode in ("RGBA", "P"):
        format = 'png'
    else:
        return_image = return_image.convert('RGB')
        format = 'jpeg'

    byte_io = io.BytesIO()
    return_image.save(byte_io, format=format.upper())
    file_size = byte_io.getbuffer().nbytes

    res = Response()
    res.headers["Content-Length"] = file_size
    res.headers["Content-Type"] = 'image/' + format

    print(str(time.time() - start_time_tile))

    return (byte_io.getvalue(), 200, res.headers.items())

def get_tile(layer_name, x, y, z):

    for _ in range(1, 3):
        try:
            return make_tile(layer_name, x, y, z)
        except Exception as _:
            pass
