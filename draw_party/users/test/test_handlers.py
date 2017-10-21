import os

from draw_party.test import BaseTestCase, mock_open, patch


class HomepageTestCase(BaseTestCase):
    def test_json_post_req_params(self):
        expected_html = b'<html>My Html</html>'

        with patch(
                'builtins.open',
                mock_open(read_data=expected_html)) as mock_file:
            resp = self.app.get('/index.html')

        mock_file.assert_called_once_with(
            os.path.join(
                os.path.dirname(os.getcwd()), 'draw_party/client/index.html'),
            'rb')
        self.assertEqual(resp.body, expected_html)
