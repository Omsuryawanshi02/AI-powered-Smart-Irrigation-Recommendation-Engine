import unittest

from fastapi.testclient import TestClient

from app.main import app


class FrontendIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())

    def test_frontend_login_page_served(self):
        response = self.client.get("/frontend/login.html")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Log in to your account", response.text)


if __name__ == "__main__":
    unittest.main()
