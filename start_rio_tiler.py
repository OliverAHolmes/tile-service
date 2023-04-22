# http://127.0.0.1:3000/wmts/tomtom_basic-main/default/GoogleMapsCompatibleExt:epsg:3857/12/2443/3366.png

from flask import Flask, Response
from rio_tiler.io import Reader
from rio_tiler.profiles import img_profiles
from PIL import Image
import io

app = Flask(__name__)

app.secret_key = b'hjlkasejd69879o'

reader_image = None

with Reader("output_cog_warp.tif") as image:
    reader_image = image


@app.route('/')
def index():
    return 'Rio Tiler Internal Tile Service'

@app.route('/<path:path>')
def tile(path):
    with Reader("output_cog_warp.tif") as image:
        req_para = path.split('/')
        layer_zoom = req_para[0]
        layer_row = req_para[1]
        layer_col = req_para[2]

        img = image.tile(int(layer_col), int(layer_row), int(layer_zoom)) 
        # img = image.tile(layer_zoom, layer_row, layer_col) 
    return_image = Image.fromarray(img.data_as_image())

    content = img.render(img_format="PNG", **img_profiles.get("png"))
    # return Response(content, media_type="image/png")
    byte_io = io.BytesIO()
    return_image.save(byte_io, format='PNG')
    file_size = byte_io.getbuffer().nbytes

    res = Response()
    res.headers["Content-Length"] = file_size
    res.headers["Content-Type"] = 'image/PNG'

    return (content, 200, res.headers.items())

@app.route('/favicon.ico')
def favicon():
    return ''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)