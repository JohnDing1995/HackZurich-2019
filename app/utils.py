from typing import List
import random
import requests

from app.config import API_KEY, PLACE_API


def get_tourist_place_ranked_list(city: str) -> List:
    places = requests.get(PLACE_API+'.json', params={'query': 'tourist+attractions+' + city,
                                                                  'key': API_KEY,
                                                                  'type': 'tourist_attraction'
                                                                  })
    print(places.json())
    places_list = [{'name': x['poi']['name'], 'address': x['address']['freeformAddress'], 'lat': x['position']['lat'], 'lon':x['position']['lon'],
                    'rating': float(hash(x['address']['freeformAddress']) % 20)/10 + 3.0} for x in places.json()['results']]
    return sorted(places_list, reverse=True, key=lambda item: item['rating'])
