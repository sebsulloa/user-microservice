import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException
from uuid import uuid4
from datetime import date
import jwt
import os

from app.routers.user import router, get_user_info_request, get_user_incidents_request, get_user_companies_request, get_user_companies_request_user, ALGORITHM, SECRET_KEY
from app.schemas.user import UserIdRequest, UserDocumentInfo, UserCompanyRequest, UserWithIncidents, UserCompaniesResponseFiltered

# Set up the FastAPI app and TestClient
app = FastAPI()
app.include_router(router)
client = TestClient(app)

class TestUserManagement(unittest.TestCase):

    def setUp(self):
        self.token = jwt.encode({"sub": "test@example.com"}, SECRET_KEY, algorithm=ALGORITHM)
    
    @patch('app.routers.user.get_user_companies_request')
    def test_get_user_companies_success(self, mock_get_user_companies_request):
        mock_get_user_companies_request.return_value = ({"companies": [{"company_name": "Test Company"}]}, 200)
        
        user_doc_info = {
            "document_type":"passport",
            "document_id":"A1234567"
        }

        response = client.post("/user-management/user/companies", json=user_doc_info)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["companies"][0]["company_name"], "Test Company")

    @patch('app.routers.user.get_user_companies_request_user')
    def test_get_user_companies_user_success(self, mock_get_user_companies_request_user):
        mock_get_user_companies_request_user.return_value = ({"companies": [{"company_name": "Test Company"}]}, 200)

        user_doc_info = UserIdRequest(
            id=uuid4()
        )

        response = client.post("/user-management/user/companies-user", data=user_doc_info.model_dump_json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["companies"][0]["company_name"], "Test Company")

    @patch('app.routers.user.get_user_info_request')
    @patch('app.routers.user.get_user_incidents_request')
    def test_get_user_with_incidents_success(self, mock_get_user_incidents_request, mock_get_user_info_request):
        # Mock the response for user info
        mock_get_user_info_request.return_value = ({
            "id": str(uuid4()),
            "username": "testuser@example.com",
            "name": "Test User",
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": date(2023, 1, 1).isoformat(),
        }, 200)

        # Mock the response for user incidents
        mock_get_user_incidents_request.return_value = ([
            {"incident_id": str(uuid4()), "description": "Test Incident"}
        ], 200)

        request_data = UserCompanyRequest(
            user_id=uuid4(),
            company_id=uuid4()
        )

        response = client.post("/user-management/user/users-view", data=request_data.model_dump_json())
        self.assertEqual(response.status_code, 200)

    def test_get_current_user_valid_token(self):
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=[ALGORITHM])
        self.assertIsNotNone(payload)
        self.assertEqual(payload["sub"], "test@example.com")

    def test_get_current_user_invalid_token(self):
        with self.assertRaises(jwt.PyJWTError):
            jwt.decode("invalid_token", SECRET_KEY, algorithms=[ALGORITHM])

if __name__ == "__main__":
    unittest.main()
