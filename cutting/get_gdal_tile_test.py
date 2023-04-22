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



def sec(x):
    return(1/cos(x))


def latlon_to_xyz(lat, lon, z):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)


def bbox_to_xyz(lon_min, lon_max, lat_min, lat_max, z):
    x_min, y_max = latlon_to_xyz(lat_min, lon_min, z)
    x_max, y_min = latlon_to_xyz(lat_max, lon_max, z)
    return(floor(x_min), floor(x_max), floor(y_min), floor(y_max))


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
    return[lon1, lat1, lon2, lat2]


start_time = time.time()

def tile2lon(x, z):
    return x / pow(2.0, z) * 360.0 - 180

def tile2lat(y, z):
    n = math.pi - (2.0 * math.pi * y) / pow(2.0, z)
    return math.degrees(math.atan(math.sinh(n)))

def tileToBbox(x, y, zoom):
    bb = {
        'north': '',
        'south': '',
        'east': '',
        'west': ''
    }

    bb['north'] = tile2lat(y, zoom)
    bb['south'] = tile2lat(y + 1, zoom)
    bb['west'] = tile2lon(x, zoom)
    bb['east'] = tile2lon(x + 1, zoom)

    polygon = str(bb['west']) + ' ' + str(bb['north']) + ','
    polygon = polygon + str(bb['east']) + ' ' + str(bb['north']) + ','
    polygon = polygon + str(bb['east']) + ' ' + str(bb['south']) + ','
    polygon = polygon + str(bb['west']) + ' ' + str(bb['south']) + ','
    polygon = polygon + str(bb['west']) + ' ' + str(bb['north'])

    return polygon

def pyproj_reproject(coord):
    proj_to = pyproj.Proj("+proj=longlat +ellps=GRS80 +towgs84=0.06155,-0.01087,-0.04019,0.0394924,0.0327221,0.03289790,-0.009994")
    lon, lat = proj_to(coord[0], coord[1], inverse=True)
    return [lon, lat]

open_file = gdal.Open('output_cog_test.tif', gdal.GA_ReadOnly)

def make_tile(x, y, z):

    print('make_tile')

    test_mem = '/vsimem/{}_{}_{}.tif'.format(x,y,z)

    tile_bounds = tileToBbox(x,y,z).split(',')[3].split( ' ')
    tile_bounds.extend(tileToBbox(x,y,z).split(',')[1].split( ' '))

    print(tile_bounds)

    # print(tile_bounds)

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
    # gdal.FileFromMemBuffer('/vsimem/cutline.geojson', cutline_geojson)

    # print(cutline_geojson)

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
    #     dstSRS=output_crs,
    #     width=256,
    #     height=256,
    #     resampleAlg="near"
    # )

    # # Perform the warp operation
    # out_ds = gdal.Warp(test_mem, open_file, options=warp_options)

    # # Delete the virtual file for the cutline GeoJSON
    # gdal.Unlink('/vsimem/cutline.geojson')

    out_ds = gdal.Warp('test_warp.png', open_file, format='PNG', outputBounds=[ tile_bounds[0],tile_bounds[1],tile_bounds[2],tile_bounds[3] ],width=256, height=256, dstSRS="EPSG:4326", resampleAlg="average", options=['COMPRESS=DEFLATE'])


    # Read the data from the GDAL dataset into a NumPy array
    data = out_ds.ReadAsArray()

    # Transpose the array so that the bands are the last axis
    data = np.transpose(data, (1, 2, 0))

    # Create a PIL Image object from the NumPy array
    return_image = Image.fromarray(data, mode='RGBA')

    return return_image


# x = 3366
# y = 2443
# z = 12 

#/20/625566/861884

y = 625566
x = 861884
z = 20

img = make_tile(x, y, z)

# return_image = Image.fromarray(img)

img.save('test_625566.png', 'PNG')

#http://localhost:8080/output_cog_test.tif/20/625566/861884

