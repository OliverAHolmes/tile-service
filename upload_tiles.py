from osgeo import gdal, osr
import services.make_tile as make_tile
import services.wasabisys as wasabisys
import os, io
import mercantile

# Open the dataset
dataset = gdal.Open("datasets/645465335874aa00066577b2.tif")

# Get the GeoTransform object
geo_transform = dataset.GetGeoTransform()

# Get raster size
x_size = dataset.RasterXSize  # number of columns
y_size = dataset.RasterYSize  # number of rows

# Calculate bounds
minx = geo_transform[0]
maxy = geo_transform[3]
maxx = minx + geo_transform[1] * x_size
miny = maxy + geo_transform[5] * y_size

# Get the existing coordinate system
old_crs = osr.SpatialReference()
old_crs.ImportFromWkt(dataset.GetProjectionRef())

# Create the new coordinate system (WGS84)
wgs84_wkt = """
GEOGCS["WGS 84",
    DATUM["WGS_1984",
        SPHEROID["WGS 84",6378137,298.257223563,
            AUTHORITY["EPSG","7030"]],
        AUTHORITY["EPSG","6326"]],
    PRIMEM["Greenwich",0,
        AUTHORITY["EPSG","8901"]],
    UNIT["degree",0.01745329251994328,
        AUTHORITY["EPSG","9122"]],
    AUTHORITY["EPSG","4326"]]"""
new_crs = osr.SpatialReference()
new_crs.ImportFromWkt(wgs84_wkt)

# Create a transform object to convert between coordinate systems
transform = osr.CoordinateTransformation(old_crs, new_crs)

# Get the corners
corner_coordinates = [(minx, miny), (minx, maxy), (maxx, miny), (maxx, maxy)]
transformed_corners = [
    transform.TransformPoint(coord[0], coord[1]) for coord in corner_coordinates
]

# Compute the bounds in the new coordinate system
minx_4326 = min([corner[0] for corner in transformed_corners])
maxx_4326 = max([corner[0] for corner in transformed_corners])
miny_4326 = min([corner[1] for corner in transformed_corners])
maxy_4326 = max([corner[1] for corner in transformed_corners])

# Your bounds (minx, miny, maxx, maxy)
bounds = (minx_4326, miny_4326, maxx_4326, maxy_4326)

# Zoom levels
zoom_levels = range(1, 22)

for z in zoom_levels:
    # Get the tiles intersecting the bounding box at each zoom level
    tiles = list(mercantile.tiles(bounds[1], bounds[0], bounds[3], bounds[2], z))

    print(f"Tiles for zoom level {z}: {len(tiles)}")

    zoom_count = len(tiles)

    for tile in tiles:
        # Get image for tile
        return_tile = make_tile.return_tile(
            "645465335874aa00066577b2.tif", tile.x, tile.y, tile.z
        )

        # Create the directories if they do not exist
        os.makedirs(f"maps/645465335874aa00066577b2/{tile.z}/{tile.x}", exist_ok=True)

        tile_key = f"maps/645465335874aa00066577b2/{tile.z}/{tile.x}/{tile.y}.png"

        # Save the image to directory
        return_tile.save(
            f"maps/645465335874aa00066577b2/{tile.z}/{tile.x}/{tile.y}.png",
            format="PNG",
        )

        # Create a BytesIO object
        img_byte_arr = io.BytesIO()

        # Write the PIL image to byte array
        return_tile.save(img_byte_arr, format="PNG")

        if(not wasabisys.test_if_tile_exists(tile_key, "ollys-documents")):
            wasabisys.upload_image(
                f"maps/645465335874aa00066577b2/{tile.z}/{tile.x}/{tile.y}.png",
                "ollys-documents",
                io.BytesIO(img_byte_arr.getvalue()),
            )
        zoom_count -= 1
        print(f"Tiles remaining: {zoom_count} in zoom level {z}")
