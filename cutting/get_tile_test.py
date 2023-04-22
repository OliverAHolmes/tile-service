from rio_tiler.io import Reader
from PIL import Image

# http://127.0.0.1:3000/wmts/tomtom_basic-main/default/GoogleMapsCompatibleExt:epsg:3857/12/2443/3366.png

with Reader("output_cog.tif") as image:

    x = 3366
    y = 2443
    z = 12

    img = image.tile(x, y, z) 

    return_image = Image.fromarray(img.data_as_image())

    return_image.save('test.png', 'PNG')