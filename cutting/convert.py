from osgeo import gdal
import numpy as np

# Open the GeoTIFF file
dataset = gdal.Open('645465335874aa00066577b2.tif', gdal.GA_ReadOnly)

# Read the data from the red, green, and blue bands
red_band = dataset.GetRasterBand(1).ReadAsArray()
green_band = dataset.GetRasterBand(2).ReadAsArray()
blue_band = dataset.GetRasterBand(3).ReadAsArray()

# Create an alpha channel array with the desired transparency
alpha_channel = np.ones_like(red_band, dtype=np.uint8) * 255  # Fully opaque

# Create an RGBA array by stacking the RGB bands with the alpha channel
rgba_array = np.dstack((red_band, green_band, blue_band, alpha_channel))

# Create a new GeoTIFF file with the RGBA array
driver = gdal.GetDriverByName('GTiff')
output_dataset = driver.Create('output.tif', dataset.RasterXSize, dataset.RasterYSize, 4, gdal.GDT_Byte)
for i in range(1, 5):  # 4 bands: red, green, blue, alpha
    output_dataset.GetRasterBand(i).WriteArray(rgba_array[:, :, i - 1])

# Close the datasets
dataset = None
output_dataset = None
