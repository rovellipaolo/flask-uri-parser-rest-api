from logging import getLogger, Logger
from urllib.parse import urlparse
import validators


class UriParser:
    def __init__(self, logger: Logger | None = None):
        self.logger = logger or getLogger("uri_parser")

    def is_valid(self, uri: str) -> bool:
        return (
            validators.url(uri) or
            validators.ip_address.ipv4(uri) or
            validators.ip_address.ipv6(uri) or
            validators.email(uri)
        )

    def parse(self, uri: str) -> dict:
        self.logger.debug("Parsing URI: %s", uri)
        info = urlparse(uri)
        return {
            "fragment": info.fragment if info.fragment != "" else None,
            "host": info.hostname,
            "port": info.port,
            "path": info.path if info.path != "" else None,
            "query": info.query if info.query != "" else None,
            "raw": uri,
            "scheme": info.scheme if info.scheme != "" else None,
            "userinfo": self._get_userinfo(username=info.username, password=info.password),
        }

    def _get_userinfo(self, username: str | None, password: str | None) -> str | None:
        if username is None or username == "":
            return None
        userinfo = username
        if password is not None and password != "":
            userinfo += f":{password}"
        return userinfo
