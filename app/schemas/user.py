from uuid import UUID
from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import date, datetime
import re
from typing import List
    
class AbcallUserCreate(BaseModel):
    username: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=1, max_length=50, pattern=r'^[a-zA-ZáéíóúñÁÉÍÓÚÑ\s]+$')
    last_name: str = Field(..., min_length=1, max_length=50, pattern=r'^[a-zA-ZáéíóúñÁÉÍÓÚÑ\s]+$')

    
class CompanyCreate(AbcallUserCreate):
    name: str = Field(..., min_length=1, max_length=100)
    birth_date: date
    phone_number: str = Field(..., pattern=r'^\+\d{2}\s\d{3}\s\d{3}\s\d{4}$')
    country: str
    city: str

    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, v: date) -> date:
        if v > date.today():
            raise ValueError('The birth date cannot be in the future.')
        return v

class CompanyResponse(BaseModel):
    id: UUID
    name: str
    first_name: str
    last_name: str
    birth_date: date
    phone_number: str
    country: str
    city: str
    username: EmailStr
    
class CompanyResponseFiltered(BaseModel):
    id: UUID
    name: str
    
class UserDocumentInfo(BaseModel):
    document_type: str
    document_id: str
    
class UserIdRequest(BaseModel):
    id: UUID
    
class UserResponse(BaseModel):
    id: UUID
    username: EmailStr
    first_name: str
    last_name: str
    document_id: str
    document_type: str
    birth_date: date
    phone_number: str
    importance: int
    allow_call: bool
    allow_sms: bool
    allow_email: bool
    registration_date: datetime
    
class IncidentResponse(BaseModel):
    id: UUID
    description: str
    state: str
    creation_date: datetime

class UserWithIncidents(UserResponse):
    incidents: List[IncidentResponse]
    
class UserCompanyRequest(BaseModel):
    user_id: UUID
    company_id: UUID
    
class UserCompaniesResponseFiltered(BaseModel):
    user_id: UUID
    companies: List[CompanyResponseFiltered]
    