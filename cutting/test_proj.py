import pyproj

# Define the input and output CRS
in_crs = 'EPSG:4326'  # WGS84 geographic coordinates
out_crs = 'EPSG:7850'  # EPSG code for the new coordinate system

# Define the input coordinate as a tuple of (longitude, latitude)
in_coord = (-32.81440132108834,115.90473175048828)

# ['115.90438842773438', '-32.81468985950556', '115.90473175048828', '-32.81440132108834']

# Create a PyProj transformer object
transformer = pyproj.Transformer.from_crs(in_crs, out_crs)

# Reproject the input coordinate
out_coord = transformer.transform(*in_coord)

print(out_coord)  # Output: (281794.778737951, 348799.0428624712)