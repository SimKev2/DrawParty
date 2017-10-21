import os

import falcon


class Homepage(object):
    """Handler for the create/join homepage."""

    MIME_TYPES = {
        'css': 'text/css',
        'html': 'text/html',
        'js': 'application/javascript'
    }
    STATIC_DIR = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'client')

    def on_get(self, req, resp, filename):
        """
        Serve static page with links.

        GET: `/`
        :param req: The request made to this endpoint.
        :type req: falcon.Request
        :param resp: The response object to be returned.
        :type resp: falcon.Response
        :param filename: The path to the file to open.
        :type filename: str
        :rtype: None
        """
        fn = os.path.join(self.STATIC_DIR, filename or 'index.html')
        resp.status = falcon.HTTP_200
        resp.set_header(
            'Content-Type', self.MIME_TYPES.get(fn.rsplit('.', 1)[-1]))

        with open(fn, 'rb') as f:
            resp.body = f.read()
