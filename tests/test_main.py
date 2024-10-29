import unittest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestMain(unittest.TestCase):

    def test_cors_headers(self):
        response = client.get("/user-management/health")
        self.assertEqual(response.status_code, 200)

    def test_api_error_exception_handler(self):
        response = client.get("/non-existent-endpoint")
        self.assertEqual(response.status_code, 404)

    def test_validation_exception_handler(self):
        response = client.post("/user-management/company/", json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("version", response.json())
        self.assertEqual(response.json()["version"], "1.0")
        self.assertIn("details", response.json())
        self.assertEqual(response.json()["message"], "Validation Error")

if __name__ == "__main__":
    unittest.main()