from flask import Flask, Response, request
from flask_cors import CORS
import io
from PIL import ImageEnhance

import services.wasabisys as wasabisys

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.secret_key = b"hjlkasejd69879o"


@app.route("/")
def index():
    return "Test Tiler Internal Tile Service"


@app.route("/<path:path>")
def tile(path):
    req_para = path.split("/")
    layer_name = req_para[0]
    layer_zoom = req_para[1]
    layer_row = req_para[2]
    layer_col = req_para[3]

    brightness = request.args.get("brightness")
    enhance = request.args.get("enhance")
    apply_overlay = request.args.get("apply_overlay")

    return_image = wasabisys.download_image(
        f"maps/{layer_name}/{layer_zoom}/{layer_col}/{layer_row}.png",
        "ollys-documents",
        (enhance == "true" if enhance is not None else False),
        (apply_overlay == "true" if apply_overlay is not None else False),
    )

    if brightness is not None:
        enhancer = ImageEnhance.Brightness(return_image)
        return_image = enhancer.enhance(float(brightness))

    if return_image.mode in ("RGBA", "P"):
        format = "png"
    else:
        return_image = return_image.convert("RGB")
        format = "jpeg"

    byte_io = io.BytesIO()
    return_image.save(byte_io, format=format.upper())
    file_size = byte_io.getbuffer().nbytes

    res = Response()
    res.headers["Content-Length"] = file_size
    res.headers["Content-Type"] = "image/" + format

    return (byte_io.getvalue(), 200, res.headers.items())


@app.route("/favicon.ico")
def favicon():
    return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
