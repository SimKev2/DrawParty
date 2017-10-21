"""Urls for the Draw Party server."""
from draw_party.users.handlers import Homepage


api_endpoints = []

endpoints = [
    ('/{filename}', Homepage())
]
