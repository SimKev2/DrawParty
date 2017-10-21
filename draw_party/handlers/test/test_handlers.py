import falcon

from draw_party import handlers
from draw_party.test import BaseTestCase, Mock, call, patch


class JsonEndpointTestCase(BaseTestCase):
    def setUp(self):
        super(JsonEndpointTestCase, self).setUp()
        self.mock_log = patch.object(
            handlers, 'log', autospec=True).start()
        self.mock_response = Mock(spec=falcon.Response)

        self.req_endpoint = handlers.JsonEndpoint(required_params={
            'group_id': int,
            'username': str
        })
        self.no_req_endpoint = handlers.JsonEndpoint()

    def test_json_post_req_params(self):
        resp = self.req_endpoint.load_params(
            Mock(falcon.Request,
                 content_length=24,
                 stream=Mock(
                     read=lambda: '{"group_id": 12, "username": "test"}')),
            self.mock_response)

        self.assertEqual(resp, {'group_id': 12, 'username': 'test'})
        self.assertEqual([
            call.debug('{"group_id": 12, "username": "test"}')],
            self.mock_log.mock_calls)

    def test_json_no_req(self):
        resp = self.no_req_endpoint.load_params(
            Mock(falcon.Request,
                 content_length=24,
                 stream=Mock(
                     read=lambda: '{"my_num": 12, "other": "test"}')),
            self.mock_response)

        self.assertEqual(resp, {'my_num': 12, 'other': 'test'})
        self.assertEqual([
            call.debug('{"my_num": 12, "other": "test"}')],
            self.mock_log.mock_calls)

    def test_json_missing_param(self):
        with self.assertRaises(handlers.MissingParameterException):
            self.req_endpoint.load_params(
                Mock(falcon.Request,
                     content_length=24,
                     stream=Mock(
                         read=lambda: '{"username": "test"}')),
                self.mock_response)

        self.assertEqual([
            call.debug('{"username": "test"}')],
            self.mock_log.mock_calls)
        self.assertEqual('400 Bad Request', self.mock_response.status)
        self.assertEqual(
            '{"error": "\\"group_id\\" required parameter is missing."}',
            self.mock_response.body)

    def test_json_bad_type(self):
        with self.assertRaises(handlers.ParameterTypeException):
            self.req_endpoint.load_params(
                Mock(falcon.Request,
                     content_length=24,
                     stream=Mock(
                         read=lambda: '{"group_id": "12", "username": "te"}')),
                self.mock_response)

        self.assertEqual([
            call.debug('{"group_id": "12", "username": "te"}')],
            self.mock_log.mock_calls)
        self.assertEqual('400 Bad Request', self.mock_response.status)
        self.assertEqual(
            '{"error": "group_id required parameter is not of type <class '
            '\'int\'>, it is of type <class \'str\'>"}',
            self.mock_response.body)

    def test_no_content(self):
        with self.assertRaises(handlers.MissingParameterException):
            self.req_endpoint.load_params(
                Mock(falcon.Request, content_length=0),
                self.mock_response)

        self.assertFalse(self.mock_log.mock_calls)
        self.assertEqual('400 Bad Request', self.mock_response.status)
        self.assertEqual(
            '{"error": "No request length."}', self.mock_response.body)
