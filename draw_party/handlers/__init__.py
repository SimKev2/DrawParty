"""Sets up base handler class."""
import json
import logging

import falcon

log = logging.getLogger(__name__)


class RequestException(Exception):
    """Exception raised for bad requests."""


class MissingParameterException(RequestException):
    """Exception for when a JSON request is missing parameters."""


class ParameterTypeException(RequestException):
    """Request for when parameters are not of the required type."""


class JsonEndpoint(object):
    """Base class for communication on endpoints using json."""

    def __init__(self, required_params=None):
        """
        Create a JsonEndpoint.

        required_params is the optional schema for the endpoint, it should be
        a dictionary where the keys are the required params and the values are
        the expected type.
        {
            'group_id': int,
            'username': str
        }

        To use required_params, just set them in the __init__ of the handler:

        >>> class MyHandler(JsonEndpoint):
        >>>   def __init__(self):
        >>>     my_params = {
        >>>       'group_id': int,
        >>>       'username': str
        >>>     }
        >>>     super(MyHandler, self).__init__(required_params=my_params)

        :param required_params: A dictionary of the required keys/types for
            the endpoint
        :type required_params: dict
        """
        self.required_params = required_params if required_params else {}

    def load_params(self, req, resp):
        """
        Parse the JSON request and verify required_params exist if defined.

        :param req: The request made to this endpoint.
        :type req: falcon.Request
        :param resp: The response object to be returned.
        :type resp: falcon.Response
        :return: The loaded request parameters.
        :rtype: dict
        """
        if not req.content_length:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'error': 'No request length.'})
            raise MissingParameterException()

        request = req.stream.read()
        log.debug(request)
        req_params = json.loads(request)

        for req_param, req_type in self.required_params.items():
            if not req_params.get(req_param):
                resp.status = falcon.HTTP_400
                resp.body = json.dumps({
                    'error': '"{}" required parameter is missing.'.format(
                        req_param)})

                raise MissingParameterException()

            if not isinstance(req_params.get(req_param), req_type):
                resp.status = falcon.HTTP_400
                resp.body = json.dumps({
                    'error': (
                        '{} required parameter is not of type {}, '
                        'it is of type {}'.format(
                            req_param, req_type, type(req_param)))})

                raise ParameterTypeException()

        return req_params
