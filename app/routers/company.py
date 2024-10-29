from typing import List
from fastapi import APIRouter, HTTPException, Path, Query, Header, Depends
from ..schemas.user import CompanyCreate, CompanyResponse
import requests
import os
from datetime import date
import jwt

router = APIRouter(prefix="/user-management/company", tags=["Company"])

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://192.168.68.111:8002/user")
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'secret_key')
ALGORITHM = "HS256"

def get_current_user(token: str = Header(None)):
    if token is None:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

def create_company_request(company: CompanyCreate):
    api_url = USER_SERVICE_URL
    endpoint = "/company/"
    company_json = company.model_dump_json()
    response = requests.post(f"{api_url}{endpoint}", data=company_json, headers={'Content-Type': 'application/json'})
    return response.json(), response.status_code

def get_company_request(company_id: str, token: str):
    api_url = USER_SERVICE_URL

    from urllib.parse import urljoin
    
    endpoint = f"company/{company_id}"
    full_url = urljoin(api_url, endpoint)
    
    headers = {"token": f"{token}"}
    response = requests.get(
        url=full_url,
        headers=headers
    )
    
    return response.json(), response.status_code

@router.post("/", response_model=CompanyResponse, status_code=201)
def create_company(company: CompanyCreate):
    response_data, status_code = create_company_request(company)
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=response_data)
    return response_data

@router.get("/{company_id}", response_model=CompanyResponse, status_code=200)
def get_company(
    company_id: str = Path(..., description="Id of the company"),
    #current_user: dict = Depends(get_current_user)
):
    #if not current_user:
    #    raise HTTPException(status_code=401, detail="Authentication required")
    
    #token = jwt.encode(current_user, SECRET_KEY, algorithm=ALGORITHM)
    response_data, status_code = get_company_request(company_id, 'token')
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response_data)
    return response_data