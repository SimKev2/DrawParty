"""Main entrypoint for the elastic beanstalk app."""
import logging

import falcon

from draw_party import urls


log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

app = application = falcon.API()

for route in urls.api_endpoints:
    app.add_route(route[0], route[1])

for route in urls.endpoints:
    app.add_route(route[0], route[1])
