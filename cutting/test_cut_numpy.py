from osgeo import gdal
import numpy as np
from PIL import Image
import io

dataset = gdal.Open("output_cog_test.tif")
# band = dataset.GetRasterBand(1)

geotransform = dataset.GetGeoTransform()

xinit = geotransform[0]
yinit = geotransform[3]

xsize = geotransform[1]
ysize = geotransform[5]

#p1 = point upper left of bounding box
#p2 = point bottom right of bounding box

# 397436.51576458476
# 6368757.117065467

p1 = (397436.51576458476, 6368757.117065467) #(6, 5) (397436.51576458476, 6368724.79513149) / 0.13 
p2 = (397468.32543943723, 6368724.79513149) #(12, 14) (397468.32543943723, 6368757.117065467) /0.25

row1 = int((p1[1] - yinit - 0.25) / ysize)
col1 = int((p1[0] - xinit + 0.25) / xsize)

row2 = int((p2[1] - yinit + 0.25) / ysize)
col2 = int((p2[0] - xinit - 0.25) / xsize)

print(row1, col1, row2, col2)

# data = band.ReadAsArray(col1, row1, col2 - col1 + 1, row2 - row1 + 1)

# Read all four bands
data = np.zeros((row2 - row1 + 1, col2 - col1 + 1, 4), dtype=np.uint8)
for i in range(4):
    band = dataset.GetRasterBand(i+1)
    data[:,:,i] = band.ReadAsArray(col1, row1, col2 - col1 + 1, row2 - row1 + 1)


# Transpose the array so that the bands are the last axis
# data = np.transpose(data, (1, 2, 0))

# Create a PIL Image object from the NumPy array
# return_image = Image.fromarray(data, 'L')
return_image = Image.fromarray(data, mode='RGBA')

return_image.save('return_image.png', 'PNG')


# [-10838991.379769664, 29225197.565127436, -10839058.192111518, 29225246.04024296]

# Set the bounding box coordinates
ulx, uly = 397436.51576458476, 6368757.117065467
lrx, lry = 397468.32543943723, 6368724.79513149

# Set the output dataset options
output_options = ['-of', 'PNG']

mem_file = '/vsimem/clipped_image.png'

# Clip the input dataset to the specified bounding box
gdal.Translate(mem_file, dataset, projWin=[ulx, uly, lrx, lry], options=output_options)
# gdal.Warp(mem_file, open_file, format='PNG',width=256, height=256, dstSRS="EPSG:4326", srcSRS="EPSG:7850", resampleAlg="near")

# Load the virtual file into a PIL image
# Read /vsimem/output.png 
f = gdal.VSIFOpenL(mem_file, 'rb')
gdal.VSIFSeekL(f, 0, 2) # seek to end
size = gdal.VSIFTellL(f)
gdal.VSIFSeekL(f, 0, 0) # seek to beginning
data = gdal.VSIFReadL(1, size, f)
gdal.VSIFCloseL(f)

return_image = Image.open(io.BytesIO(data))

# return_image = Image.fromarray(data, mode='RGBA')
# return_image = Image.open(gdal.VSIFOpenL("mem_file", "rb"));

# Delete the virtual file from memory
gdal.Unlink(mem_file)

# data = out_ds.ReadAsArray()

# # Transpose the array so that the bands are the last axis
# data = np.transpose(data, (1, 2, 0))

# # Create a PIL Image object from the NumPy array
# return_image = Image.fromarray(data, mode='RGBA')

# # Open the clipped dataset and save it as an image
# clip_ds = gdal.Open('/vsimem/clip.tif')
# clip_array = clip_ds.ReadAsArray()
# clip_image = Image.fromarray(clip_array, mode='RGBA')
return_image = return_image.resize((256, 256))
return_image.save('clip_image_test.png', 'PNG')

# Clean up the temporary dataset
gdal.Unlink('/vsimem/clip.tif')