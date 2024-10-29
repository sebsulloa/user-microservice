from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Header, Depends
from ..schemas.user import UserIdRequest, UserDocumentInfo, UserCompanyRequest, UserWithIncidents, UserCompaniesResponseFiltered
import requests
import os
import jwt

router = APIRouter(prefix="/user-management/user", tags=["User"])

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://192.168.68.111:8002/user")
QUERY_INCIDENT_SERVICE_URL = os.getenv("QUERY_INCIDENT_SERVICE_URL", "http://192.168.68.111:8006/incident-query")
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'secret_key')
ALGORITHM = "HS256"

def get_user_info_request(user_id: UUID, token: str):
    api_url = USER_SERVICE_URL
    endpoint = f"/user/{user_id}"
    headers = {"token": f"{token}"}
    response = requests.get(f"{api_url}{endpoint}", headers=headers)
    return response.json(), response.status_code

def get_user_incidents_request(user_id: UUID, company_id: UUID, token: str):
    api_url = QUERY_INCIDENT_SERVICE_URL
    endpoint = "/user-company"
    headers = {
        "token": f"{token}",
        "Content-Type": "application/json"
    }
    data = {
        "user_id": str(user_id),
        "company_id": str(company_id)
    }
    response = requests.post(f"{api_url}{endpoint}", headers=headers, json=data)
    return response.json(), response.status_code

def get_current_user(token: str = Header(None)):
    if token is None:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

def get_user_companies_request(user_doc_info: UserDocumentInfo, token: str):
    api_url = USER_SERVICE_URL
    endpoint = "user/companies"
    headers = {
        "token": f"{token}",
        "Content-Type": "application/json"
    }
    data = user_doc_info.model_dump_json()
    response = requests.post(f"{api_url}/{endpoint}", data=data, headers=headers)
    return response.json(), response.status_code

def get_user_companies_request_user(user_doc_info: UserIdRequest, token: str):
    api_url = USER_SERVICE_URL
    endpoint = "user/companies-user"
    headers = {
        "token": f"{token}",
        "Content-Type": "application/json"
    }
    data = user_doc_info.model_dump_json()
    response = requests.post(f"{api_url}/{endpoint}", data=data, headers=headers)
    return response.json(), response.status_code

@router.post("/companies")
def get_user_companies(
    user_doc_info: UserDocumentInfo,
    #current_user: dict = Depends(get_current_user)
):
    #if not current_user:
    #     raise HTTPException(status_code=401, detail="Authentication required")
    
    #token = jwt.encode(current_user, SECRET_KEY, algorithm=ALGORITHM)
    response_data, status_code = get_user_companies_request(user_doc_info, 'token')
    
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response_data)
    
    return response_data

@router.post("/companies-user")
def get_user_companies(
    user_doc_info: UserIdRequest,
    #current_user: dict = Depends(get_current_user)
):
    #if not current_user:
     #    raise HTTPException(status_code=401, detail="Authentication required")
    
    #token = jwt.encode(current_user, SECRET_KEY, algorithm=ALGORITHM)
    response_data, _ = get_user_companies_request_user(user_doc_info, 'token')
    
    return response_data



@router.post("/users-view")
async def get_user_with_incidents(
    request_data: UserCompanyRequest,
    #current_user: dict = Depends(get_current_user)
):
    #if not current_user:
    #    raise HTTPException(status_code=401, detail="Authentication required")
    
    #token = jwt.encode(current_user, SECRET_KEY, algorithm=ALGORITHM)
        
    incidents_data = get_user_incidents_request(request_data.user_id, request_data.company_id, 'token')
    
    return incidents_data