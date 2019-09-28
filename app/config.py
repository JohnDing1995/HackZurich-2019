from os import environ

DIRECTION_API = "https://maps.googleapis.com/maps/api/directions/json"
GOOGLE_API_KEY = environ.get('API_KEY', None)
