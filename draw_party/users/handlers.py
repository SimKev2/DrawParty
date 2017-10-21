import logging
import mimetypes
import os

import falcon


log = logging.getLogger(__name__)


class Homepage(object):
    """Handler for the create/join homepage."""

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
        :rtype: None
        """
        log.error(req.path)
        fn = os.path.join(self.STATIC_DIR, filename)
        resp.set_header(
            'Content-Type',
            mimetypes.guess_type(fn, strict=False)[0] or 'text/html')

        resp.status = falcon.HTTP_200
        with open(fn, 'rb') as f:
            resp.body = f.read()
