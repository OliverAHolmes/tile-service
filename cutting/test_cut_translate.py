from osgeo import gdal
import numpy as np
from PIL import Image
import io

dataset = gdal.Open("./datasets/output_cog_test.tif")

# Set the bounding box coordinates
ulx, uly = 397436.51576458476, 6368757.117065467
lrx, lry = 397468.32543943723, 6368724.79513149

# Set the output dataset options
output_options = ['-of', 'PNG']

mem_file = '/vsimem/clipped_image.png'

# Clip the input dataset to the specified bounding box
gdal.Translate(mem_file, dataset, projWin=[ulx, uly, lrx, lry], options=output_options)
gdal.Warp('./test_data/clipped_image_warp.png', mem_file, format='PNG',width=256, height=256, dstSRS="EPSG:7850", srcSRS="EPSG:7850", resampleAlg="near")

f = gdal.VSIFOpenL(mem_file, 'rb')
gdal.VSIFSeekL(f, 0, 2) # seek to end
size = gdal.VSIFTellL(f)
gdal.VSIFSeekL(f, 0, 0) # seek to beginning
data = gdal.VSIFReadL(1, size, f)
gdal.VSIFCloseL(f)

# Clean up the temporary dataset
gdal.Unlink('/vsimem/clip.tif')

return_image = Image.open(io.BytesIO(data))
gdal.Unlink(mem_file)

return_image = return_image.resize((256, 256))
return_image.save('./test_data/clip_image_test.png', 'PNG')

