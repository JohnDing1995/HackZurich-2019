import random
from datetime import datetime

import requests
from flask import Flask, render_template, jsonify
from flask import request

from app.model import db, Places
from .config import PLACE_API, SYGIC_KEY, TOMTOM_KEY, GOOGLE_KEY
from .path_finder import SiteClass, Arguments, dfs
from .utils import get_tourist_place_ranked_list, get_all_route

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def main_page():
    return render_template('main.html', api_key=GOOGLE_KEY)


@app.route('/api/route')
def get_tour_route():
    lat_lon_list = list(map(lambda x: eval(x), request.args.getlist('search-location')))
    start_time = datetime.strptime(request.args.get('start-time'), '%d/%m/%y %H:%M')
    end_time = datetime.strptime(request.args.get('end-time'), '%d/%m/%y %H:%M')
    time_duration = end_time - start_time
    site_list = [0]
    for each in lat_lon_list:
        site_list.append(SiteClass(rating=Places.query.filter_by(lat=each[0], lon=each[1]).first().rating))
    start_point = request.args.get('start')
    start_response = requests.get("https://maps.googleapis.com/maps/api/place/findplacefromtext/json", params={
        'key': GOOGLE_KEY,
        'inputtype':'textquery',
        'input':start_point,
        'fields':'geometry'
    })
    random.shuffle(lat_lon_list)
    lat_lon_list.insert(0, (
    start_response.json()['candidates'][0]['geometry']['location']['lat'], start_response.json()['candidates'][0]['geometry']['location']['lng']))
    end_point = request.args.get('end')
    end_response = requests.get("https://maps.googleapis.com/maps/api/place/findplacefromtext/json", params={
        'key': GOOGLE_KEY,
        'inputtype':'textquery',
        'input':end_point,
        'fields': 'geometry'
    })
    lat_lon_list.append(
        (end_response.json()['candidates'][0]['geometry']['location']['lat'], end_response.json()['candidates'][0]['geometry']['location']['lng']))
    # Get all route
    # all_route_mat = get_all_route(lat_lon_list, start_time)
    # argument = Arguments(len(all_route_mat)-2, end_time, all_route_mat, site_list, DESTINATION_INDEX=len(all_route_mat)-1)
    # dfs(0, start_time, 0, argument)

    return jsonify(lat_lon_list)


@app.route('/api/city/<addr>')
def get_city(addr):
    places = requests.get(PLACE_API + '.json', params={'query': addr,
                                                       'key': TOMTOM_KEY,
                                                       'limit': 1
                                                       })
    city = places.json()['results'][0]['address']['municipality']
    return jsonify({'city': city})


@app.route('/api/tourist/<city>')
def get_tourist_place(city):
    places_global = get_tourist_place_ranked_list(city)
    return jsonify(places_global)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
