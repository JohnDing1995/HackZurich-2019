import json

from flask import Flask, render_template
from flask import request
import requests
from .config import DIRECTION_API, GOOGLE_API_KEY
import googlemaps
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main.html', api_key=GOOGLE_API_KEY)

@app.route('/arrive_time')
def get_arrive_time():
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
    origin  = request.args.get('from')
    destination = request.args.get('to')
    method = requests.args.get('method', 'transit')
    leave_at = request.args.get('leave_at', datetime.now())
    directions_result = gmaps.directions(origin,
                                         destination,
                                         mode="transit",
                                         departure_time=leave_at)
    print(directions_result)
    return json.dumps(directions_result)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
