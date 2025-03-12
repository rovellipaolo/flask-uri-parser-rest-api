import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized

from uri_parser.uri_parser import UriParser


class TestUriParser(unittest.TestCase):
    ANY_URI = "domain.tld"

    sut = UriParser()

    @staticmethod
    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def _any_urlparse(
        fragment: str = "",
        host: str | None = None,
        port: str | None = None,
        path: str = "",
        password: str | None = None,
        query: str = "",
        scheme: str = "",
        username: str | None = None
    ):
        info = MagicMock()
        info.fragment = fragment
        info.hostname = host
        info.port = port
        info.path = path
        info.password = password
        info.query = query
        info.scheme = scheme
        info.username = username
        return info

    @parameterized.expand([
        [False, False, False, False, False],
        [True, False, False, False, True],
        [False, True, False, False, True],
        [False, False, True, False, True],
        [False, False, False, True, True]
    ])
    @patch("uri_parser.uri_parser.validators")
    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def test_is_valid(self, is_url, is_ipv4, is_ipv6, is_email, expected_result, mock_validators):
        mock_validators.url.return_value = is_url
        mock_validators.ip_address.ipv4.return_value = is_ipv4
        mock_validators.ip_address.ipv6.return_value = is_ipv6
        mock_validators.email.return_value = is_email

        result = self.sut.is_valid(self.ANY_URI)

        self.assertEqual(expected_result, result)

    @parameterized.expand([
        [
            "",
            None,
            None,
            "",
            None,
            "",
            "",
            None,
            {
                "fragment": None,
                "host": None,
                "port": None,
                "path": None,
                "query": None,
                "raw": ANY_URI,
                "scheme": None,
                "userinfo": None
            }
        ],
        [
            "",
            "any-host",
            "",
            "",
            "",
            "",
            "any-scheme",
            "",
            {
                "fragment": None,
                "host": "any-host",
                "port": "",
                "path": None,
                "query": None,
                "raw": ANY_URI,
                "scheme": "any-scheme",
                "userinfo": None
            }
        ],
        [
            "any-fragment",
            "any-host",
            80,
            "any-path",
            None,
            "any-query",
            "any-scheme",
            "any-username",
            {
                "fragment": "any-fragment",
                "host": "any-host",
                "port": 80,
                "path": "any-path",
                "query": "any-query",
                "raw": ANY_URI,
                "scheme": "any-scheme",
                "userinfo": "any-username"
            }
        ],
        [
            "any-fragment",
            "any-host",
            80,
            "any-path",
            "any-password",
            "any-query",
            "any-scheme",
            None,
            {
                "fragment": "any-fragment",
                "host": "any-host",
                "port": 80,
                "path": "any-path",
                "query": "any-query",
                "raw": ANY_URI,
                "scheme": "any-scheme",
                "userinfo": None
            }
        ],
        [
            "any-fragment",
            "any-host",
            80,
            "any-path",
            "any-password",
            "any-query",
            "any-scheme",
            "any-username",
            {
                "fragment": "any-fragment",
                "host": "any-host",
                "port": 80,
                "path": "any-path",
                "query": "any-query",
                "raw": ANY_URI,
                "scheme": "any-scheme",
                "userinfo": "any-username:any-password"
            }
        ]
    ])
    @patch("uri_parser.uri_parser.urlparse")
    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def test_parse(
        self,
        fragment,
        host,
        port,
        path,
        password,
        query,
        scheme,
        username,
        expected_result,
        mock_urlparse
    ):
        mock_urlparse.return_value = self._any_urlparse(
            fragment=fragment,
            host=host,
            port=port,
            path=path,
            password=password,
            query=query,
            scheme=scheme,
            username=username
        )

        result = self.sut.parse(self.ANY_URI)

        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
