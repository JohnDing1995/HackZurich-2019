from datetime import datetime
from typing import List
import random

import googlemaps
import requests

from .model import db
from .model import Places
from app.config import SYGIC_KEY, TOMTOM_KEY, DIRECTION_API, PLACE_API, GOOGLE_KEY, GOOGLE_PLACE_API


def get_tourist_place_ranked_list(city: str) -> List:
    places = requests.get(GOOGLE_PLACE_API, params={'query': 'tourist+attractions+{}'.format(city),
                                                    'key': GOOGLE_KEY,

                                                    })
    print(places.json())
    places_list = [{'name':x['name'], 'address': x['formatted_address'], 'lat': x['geometry']['location']['lat'],
                    'lon': x['geometry']['location']['lng'],
                    'rating': x['rating']} for x in
                   places.json()['results']][:10]
    db.session.query(Places).delete()
    db.session.commit()
    for id, each in enumerate(places_list):
        p = Places(id=id, name=each['name'], lat=each['lat'], lon=each['lon'], address=each['address'],
                   rating=each['rating'])
        db.session.add(p)
        db.session.commit()
    return sorted(places_list, reverse=True, key=lambda item: item['rating'])


def get_route(start, end, leave_at=datetime.now(), method="transit"):
    gmaps = googlemaps.Client(key=GOOGLE_KEY)
    directions_result = gmaps.directions(start,
                                         end,
                                         mode=method,
                                         departure_time=leave_at)
    return directions_result


def get_all_route(points, start_time):
    all_route_info = [[0 for x in range(len(points))] for y in range(len(points))]
    for i in range(0, len(points) - 1):
        for j in range(0, len(points)):
            if points[i] != points[j]:
                route = get_route(points[i], points[j], start_time)
                all_route_info[i][j] = route[0]['legs'][0]['duration']['value']
    print(all_route_info)
    return all_route_info
