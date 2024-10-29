import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from datetime import date
import json
import jwt
import os

# Mock the environment variable
os.environ['JWT_SECRET_KEY'] = 'test_secret_key'

from app.routers.company import router, create_company_request, get_company_request, get_current_user, ALGORITHM
from app.schemas.user import CompanyCreate, CompanyResponse

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def json_serializable(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

class TestCompanyManagement(unittest.TestCase):

    def setUp(self):
        self.secret_key = 'test_secret_key'
        self.valid_token = jwt.encode({"sub": "test@example.com"}, self.secret_key, algorithm=ALGORITHM)

    @patch('app.routers.company.create_company_request')
    def test_create_company_success(self, mock_create_company_request):
        mock_create_company_request.return_value = ({
            "id": "12345678-1234-5678-1234-567812345678",
            "username": "testuser@example.com",
            "name": "Test Company",
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": "2023-01-01",
            "phone_number": "+12 345 678 9012",
            "country": "TestCountry",
            "city": "TestCity"
        }, 201)

        company_data = CompanyCreate(
            username="testuser@example.com",
            password="testpass",
            name="Test Company",
            first_name="John",
            last_name="Doe",
            birth_date=date(2023, 1, 1),
            phone_number="+12 345 678 9012",
            country="TestCountry",
            city="TestCity"
        )
        response = client.post("/user-management/company/", json=json.loads(json.dumps(company_data.dict(), default=json_serializable)))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Test Company")

    @patch('app.routers.company.create_company_request')
    def test_create_company_failure(self, mock_create_company_request):
        mock_create_company_request.return_value = ({"detail": "Error creating company"}, 400)

        company_data = CompanyCreate(
            username="testuser@example.com",
            password="testpass",
            name="Test Company",
            first_name="John",
            last_name="Doe",
            birth_date=date(2023, 1, 1),
            phone_number="+12 345 678 9012",
            country="TestCountry",
            city="TestCity"
        )
        response = client.post("/user-management/company/", json=json.loads(json.dumps(company_data.dict(), default=json_serializable)))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": {"detail": "Error creating company"}})

    #def test_get_company_unauthorized(self):
    #    response = client.get("/user-management/company/12345678-1234-5678-1234-567812345678")
    #    self.assertEqual(response.status_code, 401)
    #    self.assertEqual(response.json(), {"detail": "Authentication required"})

    #def test_get_company_invalid_token(self):
    #    response = client.get("/user-management/company/12345678-1234-5678-1234-567812345678", headers={"Authorization": "Bearer invalid_token"})
    #    self.assertEqual(response.status_code, 401)
    #    self.assertEqual(response.json(), {"detail": "Authentication required"})

    @patch('requests.post')
    def test_create_company_request(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "12345678-1234-5678-1234-567812345678",
            "username": "testuser@example.com",
            "name": "Test Company",
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": "2023-01-01",
            "phone_number": "+12 345 678 9012",
            "country": "TestCountry",
            "city": "TestCity"
        }
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        company = CompanyCreate(
            username="testuser@example.com",
            password="testpass",
            name="Test Company",
            first_name="John",
            last_name="Doe",
            birth_date=date(2023, 1, 1),
            phone_number="+12 345 678 9012",
            country="TestCountry",
            city="TestCity"
        )

        response_data, status_code = create_company_request(company)
        self.assertEqual(status_code, 201)
        self.assertEqual(response_data["name"], "Test Company")

    @patch('requests.get')
    def test_get_company_request(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "12345678-1234-5678-1234-567812345678",
            "username": "testuser@example.com",
            "name": "Test Company",
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": "2023-01-01",
            "phone_number": "+12 345 678 9012",
            "country": "TestCountry",
            "city": "TestCity"
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response_data, status_code = get_company_request("12345678-1234-5678-1234-567812345678", self.valid_token)
        self.assertEqual(status_code, 200)
        self.assertEqual(response_data["name"], "Test Company")

    def test_get_current_user_valid_token(self):
        token = jwt.encode({"sub": "test@example.com"}, self.secret_key, algorithm=ALGORITHM)
        user = get_current_user(token)
        self.assertIsNotNone(user)
        self.assertEqual(user["sub"], "test@example.com")

    def test_get_current_user_invalid_token(self):
        user = get_current_user("invalid_token")
        self.assertIsNone(user)

    def test_get_current_user_no_token(self):
        user = get_current_user(None)
        self.assertIsNone(user)