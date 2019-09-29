from os import environ

PLACE_API = "https://api.tomtom.com/search/2/search/.json"
DIRECTION_API = "https://routing.api.sygic.com/v0/api/directions"
TOMTOM_KEY = environ.get('TOMTOM_KEY', None)
SYGIC_KEY = environ.get('SYGIC_KEY', None)
GOOGLE_KEY = environ.get('GOOGLE_KEY', None)
GOOGLE_PLACE_API = "https://maps.googleapis.com/maps/api/place/textsearch/json"