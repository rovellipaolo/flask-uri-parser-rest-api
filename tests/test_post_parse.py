import sys
import unittest
from parameterized import parameterized

# Inject uri_parser.py (in production this is not needed):
sys.path.append("src")

# pylint: disable-next=wrong-import-position
from src.app import app  # noqa: E402


class TestPostParse(unittest.TestCase):
    def setUp(self):
        self.sut = app.test_client()

    def tearDown(self):
        self.sut = None

    @parameterized.expand([
        # GENERIC
        [
            "127.0.0.1",
            "false",
            {
                "fragment": None,
                "host": None,
                "port": None,
                "path": "127.0.0.1",
                "query": None,
                "raw": "127.0.0.1",
                "scheme": None,
                "userinfo": None
            }
        ],
        [
            "domain.tld",
            "true",
            {
                "fragment": None,
                "host": None,
                "port": None,
                "path": "domain.tld",
                "query": None,
                "raw": "domain.tld",
                "scheme": None,
                "userinfo": None
            }
        ],
        [
            "username@domain.tld",
            "false",
            {
                "fragment": None,
                "host": None,
                "port": None,
                "path": "username@domain.tld",
                "query": None,
                "raw": "username@domain.tld",
                "scheme": None,
                "userinfo": None
            }
        ],
        # HTTP
        [
            "http://127.0.0.1",
            "false",
            {
                "fragment": None,
                "host": "127.0.0.1",
                "port": None,
                "path": None,
                "query": None,
                "raw": "http://127.0.0.1",
                "scheme": "http",
                "userinfo": None
            }
        ],
        [
            "http://domain.tld",
            "false",
            {
                "fragment": None,
                "host": "domain.tld",
                "port": None,
                "path": None,
                "query": None,
                "raw": "http://domain.tld",
                "scheme": "http",
                "userinfo": None
            }
        ],
        [
            "http://user:password@domain.tld:8080/path?key=value#fragment",
            "false",
            {
                "fragment": "fragment",
                "host": "domain.tld",
                "port": 8080,
                "path": "/path",
                "query": "key=value",
                "raw": "http://user:password@domain.tld:8080/path?key=value#fragment",
                "scheme": "http",
                "userinfo": "user:password"
            }
        ],
        # HTTPS
        [
            "https://127.0.0.1",
            "false",
            {
                "fragment": None,
                "host": "127.0.0.1",
                "port": None,
                "path": None,
                "query": None,
                "raw": "https://127.0.0.1",
                "scheme": "https",
                "userinfo": None
            }
        ],
        [
            "https://domain.tld",
            "false",
            {
                "fragment": None,
                "host": "domain.tld",
                "port": None,
                "path": None,
                "query": None,
                "raw": "https://domain.tld",
                "scheme": "https",
                "userinfo": None
            }
        ],
        [
            "https://user:password@domain.tld:8080/path?key=value#fragment",
            "false",
            {
                "fragment": "fragment",
                "host": "domain.tld",
                "port": 8080,
                "path": "/path",
                "query": "key=value",
                "raw": "https://user:password@domain.tld:8080/path?key=value#fragment",
                "scheme": "https",
                "userinfo": "user:password"
            }
        ],
        # FTP
        [
            "ftp://domain.tld",
            "false",
            {
                "fragment": None,
                "host": "domain.tld",
                "port": None,
                "path": None,
                "query": None,
                "raw": "ftp://domain.tld",
                "scheme": "ftp",
                "userinfo": None
            }
        ],
        # MAILTO
        [
            "mailto:username@domain.tld",
            "true",
            {
                "fragment": None,
                "host": None,
                "port": None,
                "path": "username@domain.tld",
                "query": None,
                "raw": "mailto:username@domain.tld",
                "scheme": "mailto",
                "userinfo": None
            }
        ]
    ])
    def test_handler(self, uri, force, expected_response_body):
        response = self.sut.post(f"/api/parse?force={force}", data=f'{{"uri": "{uri}"}}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response_body, response.get_json())

    def test_handler_when_request_has_invalid_uri(self):
        invalid_uri = "not-a-uri"
        response = self.sut.post("/api/parse", data=f'{{"uri": "{invalid_uri}"}}')

        self.assertEqual(response.status_code, 400)
        self.assertEqual({"error": "Bad Request", "message": f"Not a valid URI: {invalid_uri}"}, response.get_json())

    @parameterized.expand([[None], ["not-a-json"], ["{}"], ['{"uri": null}'], ['{"uri": ""}']])
    def test_handler_when_request_has_invalid_or_empty_body(self, request_body):
        response = self.sut.post("/api/parse", data=request_body)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            {"error": "Bad Request", "message": "Missing 'uri' parameter in request!"},
            response.get_json()
        )


if __name__ == '__main__':
    unittest.main()
