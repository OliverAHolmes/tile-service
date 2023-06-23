import io
from flask import Response
import make_tile as make_tile_service

def make_tile(layer_name, x, y, z):

    return_image = make_tile_service.return_tile(layer_name, x, y, z)

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

    return (byte_io.getvalue(), 200, res.headers.items())

def get_tile(layer_name, x, y, z):

    for _ in range(1, 3):
        try:
            return make_tile(layer_name, x, y, z)
        except Exception as _:
            pass
