from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

# Employee Models
class Employee(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    title: str
    department: str
    grade: str
    basic_salary: float
    total_salary: float
    bank_account: str
    start_date: str
    manager: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EmployeeCreate(BaseModel):
    name: str
    email: str
    title: str
    department: str
    grade: str
    basic_salary: float
    total_salary: float
    bank_account: str
    start_date: str
    manager: str

# HR Request Models
class HRRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_id: str
    type: str  # vacation, sick, wfh, certificate, expense, travel
    status: str = "Pending Approval"  # Pending Approval, Under Review, Approved, Rejected
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    date: Optional[str] = None  # For single day requests like WFH
    days: Optional[int] = None
    reason: Optional[str] = None
    purpose: Optional[str] = None  # For certificates
    amount: Optional[float] = None  # For expenses
    category: Optional[str] = None  # For expenses
    description: Optional[str] = None
    destination: Optional[str] = None  # For travel
    duration: Optional[int] = None  # For travel
    departure_date: Optional[str] = None
    return_date: Optional[str] = None
    business_purpose: Optional[str] = None
    details: Optional[str] = None
    submitted_date: datetime = Field(default_factory=datetime.utcnow)
    approved_date: Optional[datetime] = None
    approved_by: Optional[str] = None

class HRRequestCreate(BaseModel):
    employee_id: str
    type: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    date: Optional[str] = None
    days: Optional[int] = None
    reason: Optional[str] = None
    purpose: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    destination: Optional[str] = None
    duration: Optional[int] = None
    departure_date: Optional[str] = None
    return_date: Optional[str] = None
    business_purpose: Optional[str] = None
    details: Optional[str] = None

# Policy Models
class Policy(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    category: str
    content: str
    tags: List[str]
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PolicyCreate(BaseModel):
    title: str
    category: str
    content: str
    tags: List[str]

# Chat Models
class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_id: str
    session_id: str
    message: str
    response: str
    type: str = "query"  # query, action, policy
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatMessageCreate(BaseModel):
    employee_id: str
    session_id: str
    message: str

# Dashboard Models
class VacationBalance(BaseModel):
    employee_id: str
    total_days: int
    used_days: int
    remaining_days: int
    year: int

class SalaryPayment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_id: str
    amount: float
    date: datetime
    status: str = "Paid"
    description: str = "Monthly Salary"

# Session Models
class Session(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_id: str
    session_token: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    is_active: bool = True

# Response Models
class EmployeeResponse(BaseModel):
    id: str
    name: str
    email: str
    title: str
    department: str
    grade: str

class DashboardData(BaseModel):
    vacation_days_left: int
    pending_requests: List[Dict[str, Any]]
    last_salary_payment: Dict[str, Any]
    business_trip_status: Dict[str, Any]
    upcoming_events: List[Dict[str, Any]]