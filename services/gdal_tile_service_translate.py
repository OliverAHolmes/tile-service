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


def sec(x):
    return(1/cos(x))

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
    return[str(lon1), str(lat1), str(lon2), str(lat2)]

in_crs = 'EPSG:4326'  # WGS84 geographic coordinates
out_crs = 'EPSG:3875'  # EPSG code for the new coordinate system

transformer = pyproj.Transformer.from_crs(in_crs, out_crs)

def make_tile(layer_name, x, y, z):

    open_file = gdal.Open(layer_name, gdal.GA_ReadOnly)
    mem_file = '/vsimem/{}_{}_{}.tif'.format(x,y,z)

    start_time_tile = time.time()

    tile_bounds = tile_edges(x,y,z)

    print(tile_bounds)


    in_coord = (tile_bounds[1],tile_bounds[0])
    out_coord = transformer.transform(*in_coord)
    print(out_coord)

    tile_bounds[0] = out_coord[0]
    tile_bounds[1] = out_coord[1]

    in_coord = (tile_bounds[3],tile_bounds[2])
    out_coord = transformer.transform(*in_coord)

    tile_bounds[2] = out_coord[0]
    tile_bounds[3] = out_coord[1]

    print(tile_bounds)

    output_options = ['-of', 'PNG']

    # 12902417.500481173, -3870694.6753330394
    # 12902455.718995323, -3870732.8938471824
    tile_bounds = [ 12902455.718995323, -3870732.8938471824 , 12902417.500481173,-3870694.6753330394 ]

    # Clip the input dataset to the specified bounding box
    # out_ds = gdal.Translate(mem_file, open_file, projWin=[tile_bounds[2], tile_bounds[3], tile_bounds[0], tile_bounds[1]], options=output_options)
    out_ds = gdal.Translate(mem_file, open_file, projWin=[tile_bounds[2], tile_bounds[3], tile_bounds[0], tile_bounds[1]], options=output_options)

    # gdal.Warp(mem_file, mem_file, format='PNG',width=256, height=256, dstSRS="EPSG:4326", srcSRS="EPSG:7850", resampleAlg="near")

    # out_ds = gdal.Warp(mem_file, open_file, format='GTiff', outputBounds=[ tile_bounds[2],tile_bounds[3],tile_bounds[0],tile_bounds[2] ],width=256, height=256, dstSRS="EPSG:3857", resampleAlg="near", options=['COMPRESS=DEFLATE'], targetAlignedPixels=False)

    # f = gdal.VSIFOpenL(mem_file, 'rb')
    # gdal.VSIFSeekL(f, 0, 2) # seek to end
    # size = gdal.VSIFTellL(f)
    # gdal.VSIFSeekL(f, 0, 0) # seek to beginning
    # data = gdal.VSIFReadL(1, size, f)
    # gdal.VSIFCloseL(f)

    # return_image = Image.open(io.BytesIO(data))
    # return_image = return_image.resize((256, 256))

    data = out_ds.ReadAsArray()

    # Transpose the array so that the bands are the last axis
    data = np.transpose(data, (1, 2, 0))

    # Create a PIL Image object from the NumPy array
    return_image = Image.fromarray(data, mode='RGBA')

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
