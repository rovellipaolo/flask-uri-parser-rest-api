import sys
import unittest

# Inject uri_parser.py (in production this is not needed):
sys.path.append("src")

# pylint: disable-next=wrong-import-position
from src.app import app  # noqa: E402


class TestGetStatus(unittest.TestCase):
    def setUp(self):
        self.sut = app.test_client()

    def tearDown(self):
        self.sut = None

    def test_get_status(self):
        response = self.sut.get("/api/status")

        self.assertEqual(200, response.status_code)
        self.assertEqual({"message": "REST API up and running... long live and prosper!"}, response.get_json())


if __name__ == '__main__':
    unittest.main()
