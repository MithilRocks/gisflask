import sqlite3
import gzip
from io import BytesIO
import mapbox_vector_tile as mvt
import geopandas as gpd
import json
import matplotlib
from flask import Flask, make_response, request
import base64
from os import environ

app = Flask(__name__)

@app.route('/tile', methods=['GET'])
def index():
    '''
    This function returns a tile from the mbtiles file as a png image
    '''

    # get the path to the mbtiles file from the environment
    MBTILES = environ.get('MBTILES')

    try:
        # connect to the mbtiles file
        con = sqlite3.connect(MBTILES)
        cursor = con.cursor()
    except sqlite3.OperationalError:
        # return a 500 error if the file is not found
        return make_response(f'Error connecting to the mbtiles file: {MBTILES}', 500)

    # get the tile data
    zoom = request.args.get('zoom')
    col = request.args.get('col')
    row = request.args.get('row')

    # return a 400 error if the tile info is not passed as parameters
    if not zoom or not col or not row:
        return make_response('No tile info passed as parameters', 400)

    try:
        # get the tile data
        cursor.execute(f'SELECT tile_data FROM tiles WHERE zoom_level={zoom} AND tile_column={col} AND tile_row={row}')
        data = cursor.fetchall()
        tile_data = data[0][0]
    except IndexError:
        return make_response('Tile not found', 404)
    except sqlite3.OperationalError:
        return make_response('No such table: tiles', 500)

    # decode the tile data
    raw_tile = BytesIO(tile_data)
    with gzip.GzipFile(fileobj=raw_tile, mode='rb') as f:
        tile = f.read()
    decoded_data = mvt.decode(tile)

    # unpack layers
    layers = [{'name': key, **decoded_data[key]} for key in decoded_data]

    # this list will contain features ready to be stored in a geojson dict
    features = []

    # unpack features for each layer into the list
    for layer in layers:
        for feature in layer['features']:
            features.append({'layer': layer['name'], 'geometry': feature['geometry'], 'id': feature['id'], 'properties': {'layer': layer['name'], 'id': feature['id'], **feature['properties']},'type': 'Feature'})

    # write to a json file ready to be loaded by geopandas
    with open('mytile.json', 'w') as file:
        data = json.dumps({'type': 'FeatureCollection', 'features': features})
        file.write(data)
    
    matplotlib.use('Agg')
    
    # read the saved geojson as a geodataframe
    feature_df = gpd.read_file('mytile.json', driver='GeoJSON')
    cmap = matplotlib.colormaps.get_cmap('viridis')

    # plot the geodataframe and save it as a base64 string
    try:
        buf = BytesIO()
        feature_df.plot(aspect=1, figsize=(10,10), cmap=cmap).get_figure().savefig(buf, format='png')
        data = base64.b64encode(buf.getbuffer()).decode('utf-8')
    except:
        return make_response('Error plotting the tile', 500)
    return make_response(f'<img src="data:image/png;base64,{data}">', 200)

if __name__ == '__main__':
    app.run(debug=True)