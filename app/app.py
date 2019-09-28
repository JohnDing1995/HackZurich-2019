import json

from flask import Flask, render_template, jsonify
from flask import request
from .utils import get_tourist_place_ranked_list
import requests
from .config import DIRECTION_API, PLACE_API, API_KEY
import googlemaps
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def main_page():
        return render_template('main.html', api_key=API_KEY)


@app.route('/api/route')
def get_arrive_time():
    gmaps = googlemaps.Client(key=API_KEY)
    origin = request.args.get('from')
    destination = request.args.get('to')
    method = request.args.get('method', 'transit')
    leave_at = request.args.get('leave_at', datetime.now())
    directions_result = gmaps.directions(origin,
                                         destination,
                                         mode=method,
                                         departure_time=leave_at)
    return jsonify(json.dumps(directions_result))


@app.route('/api/tourist/<city>')
def get_tourist_place(city):
    return jsonify(get_tourist_place_ranked_list(city))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
