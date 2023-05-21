from flask import Flask, request, Response, session, escape, render_template, redirect, jsonify, send_file

import services.gdal_tile_service as ts

app = Flask(__name__)

app.secret_key = b'hjlkasejd69879o'

@app.route('/')
def index():
    return 'Test Tiler Internal Tile Service'

@app.route('/<path:path>')
def tile(path):

    req_para = path.split('/')
    layer_name = req_para[0]
    layer_zoom = req_para[1]
    layer_row = req_para[2]
    layer_col = req_para[3]

    return ts.get_tile(str(layer_name), int(layer_col),int(layer_row),int(layer_zoom))

@app.route('/favicon.ico')
def favicon():
    return ''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)