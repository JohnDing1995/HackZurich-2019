from os import environ

PLACE_API = "https://api.tomtom.com/search/2/search/.json"
DIRECTION_API = "https://maps.googleapis.com/maps/api/place"
API_KEY = environ.get('API_KEY', None)
