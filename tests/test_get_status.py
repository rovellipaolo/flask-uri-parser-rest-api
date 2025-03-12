import unittest
from app import app


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
