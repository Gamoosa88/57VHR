from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables first, before other imports
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import asyncio

# Import models and services
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import *
from database import *
from ai_service import AIHRAssistant

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize AI service
ai_assistant = AIHRAssistant()

# Create the main app
app = FastAPI(title="1957 Ventures HR Hub API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_db():
    await init_database()

# Basic health check
@api_router.get("/")
async def root():
    return {"message": "1957 Ventures HR Hub API", "status": "running"}

# Employee endpoints
@api_router.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: str):
    employee = await employees_collection.find_one({"id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return Employee(**employee)

@api_router.get("/employees", response_model=List[Employee])
async def get_employees():
    employees = await employees_collection.find().to_list(100)
    return [Employee(**emp) for emp in employees]

# Dashboard endpoints
@api_router.get("/dashboard/{employee_id}")
async def get_dashboard_data(employee_id: str):
    # Get employee
    employee = await employees_collection.find_one({"id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Get vacation balance
    vacation_balance = await vacation_balances_collection.find_one({"employee_id": employee_id})
    vacation_days_left = vacation_balance["remaining_days"] if vacation_balance else 0
    
    # Get pending requests
    pending_requests = await hr_requests_collection.find({
        "employee_id": employee_id,
        "status": {"$in": ["Pending Approval", "Under Review"]}
    }).sort("submitted_date", -1).to_list(10)
    
    # Format pending requests
    formatted_requests = []
    for req in pending_requests:
        formatted_req = {
            "id": req["id"],
            "type": req["type"],
            "status": req["status"],
            "submittedDate": req["submitted_date"].isoformat(),
            "startDate": req.get("start_date") or req.get("departure_date"),
            "destination": req.get("destination"),
            "amount": req.get("amount")
        }
        formatted_requests.append(formatted_req)
    
    # Get last salary payment
    last_salary = await salary_payments_collection.find_one(
        {"employee_id": employee_id},
        sort=[("date", -1)]
    )
    
    salary_payment = {
        "amount": last_salary["amount"],
        "date": last_salary["date"].isoformat(),
        "status": last_salary["status"]
    } if last_salary else {"amount": 0, "date": "", "status": ""}
    
    # Get business trip status
    business_trip = await hr_requests_collection.find_one({
        "employee_id": employee_id,
        "type": "Business Trip",
        "status": {"$in": ["Approved", "Pending Approval"]}
    }, sort=[("submitted_date", -1)])
    
    trip_status = {
        "current": business_trip.get("destination", "No active trip"),
        "status": business_trip.get("status", "None"),
        "startDate": business_trip.get("departure_date", ""),
        "endDate": business_trip.get("return_date", "")
    } if business_trip else {
        "current": "No active trip",
        "status": "None",
        "startDate": "",
        "endDate": ""
    }
    
    # Mock upcoming events (could be enhanced with actual event system)
    upcoming_events = [
        {"type": "Performance Review", "date": "2025-01-30"},
        {"type": "Team Meeting", "date": "2025-01-15"}
    ]
    
    return {
        "vacationDaysLeft": vacation_days_left,
        "pendingRequests": formatted_requests,
        "lastSalaryPayment": salary_payment,
        "businessTripStatus": trip_status,
        "upcomingEvents": upcoming_events
    }

# HR Request endpoints
@api_router.post("/hr-requests", response_model=HRRequest)
async def create_hr_request(request: HRRequestCreate):
    # Validate employee exists
    employee = await employees_collection.find_one({"id": request.employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Create request
    request_dict = request.dict()
    request_dict["id"] = str(uuid.uuid4())
    request_dict["submitted_date"] = datetime.utcnow()
    request_dict["status"] = "Pending Approval"
    
    # Calculate days for vacation/sick leave
    if request.start_date and request.end_date:
        start = datetime.fromisoformat(request.start_date)
        end = datetime.fromisoformat(request.end_date)
        request_dict["days"] = (end - start).days + 1
    
    await hr_requests_collection.insert_one(request_dict)
    
    # Update vacation balance if it's a vacation request
    if request.type == "Vacation Leave" and request_dict.get("days"):
        await vacation_balances_collection.update_one(
            {"employee_id": request.employee_id},
            {"$inc": {"used_days": request_dict["days"], "remaining_days": -request_dict["days"]}}
        )
    
    return HRRequest(**request_dict)

@api_router.get("/hr-requests/{employee_id}", response_model=List[HRRequest])
async def get_hr_requests(employee_id: str):
    requests = await hr_requests_collection.find(
        {"employee_id": employee_id}
    ).sort("submitted_date", -1).to_list(50)
    return [HRRequest(**req) for req in requests]

@api_router.put("/hr-requests/{request_id}/status")
async def update_request_status(request_id: str, status: str, approved_by: Optional[str] = None):
    update_data = {"status": status}
    if status == "Approved":
        update_data["approved_date"] = datetime.utcnow()
        if approved_by:
            update_data["approved_by"] = approved_by
    
    result = await hr_requests_collection.update_one(
        {"id": request_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Request not found")
    
    return {"message": "Request status updated successfully"}

# Policy endpoints
@api_router.get("/policies", response_model=List[Policy])
async def get_policies(category: Optional[str] = None, search: Optional[str] = None):
    query = {}
    
    if category and category != "all":
        query["category"] = category
    
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"content": {"$regex": search, "$options": "i"}},
            {"tags": {"$regex": search, "$options": "i"}}
        ]
    
    policies = await policies_collection.find(query).to_list(100)
    return [Policy(**policy) for policy in policies]

@api_router.get("/policies/{policy_id}", response_model=Policy)
async def get_policy(policy_id: str):
    policy = await policies_collection.find_one({"id": policy_id})
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return Policy(**policy)

@api_router.get("/policies/categories")
async def get_policy_categories():
    categories = await policies_collection.distinct("category")
    return {"categories": categories}

# Chat endpoints
@api_router.post("/chat/message")
async def send_chat_message(message_data: ChatMessageCreate):
    try:
        # Generate AI response
        ai_response = await ai_assistant.generate_response(
            message_data.message,
            message_data.employee_id,
            message_data.session_id
        )
        
        # Save message to database
        chat_message = {
            "id": str(uuid.uuid4()),
            "employee_id": message_data.employee_id,
            "session_id": message_data.session_id,
            "message": message_data.message,
            "response": ai_response["response"],
            "type": ai_response["type"],
            "timestamp": datetime.utcnow()
        }
        
        await chat_messages_collection.insert_one(chat_message)
        
        return {
            "id": chat_message["id"],
            "message": message_data.message,
            "response": ai_response["response"],
            "type": ai_response["type"],
            "timestamp": chat_message["timestamp"].isoformat()
        }
        
    except Exception as e:
        print(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process chat message")

@api_router.get("/chat/history/{employee_id}")
async def get_chat_history(employee_id: str, session_id: Optional[str] = None):
    query = {"employee_id": employee_id}
    if session_id:
        query["session_id"] = session_id
    
    messages = await chat_messages_collection.find(query).sort("timestamp", -1).limit(50).to_list(50)
    
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "id": msg["id"],
            "message": msg["message"],
            "response": msg["response"],
            "type": msg["type"],
            "timestamp": msg["timestamp"].isoformat()
        })
    
    return {"messages": list(reversed(formatted_messages))}

# Additional utility endpoints
@api_router.get("/vacation-balance/{employee_id}")
async def get_vacation_balance(employee_id: str):
    balance = await vacation_balances_collection.find_one({"employee_id": employee_id})
    if not balance:
        raise HTTPException(status_code=404, detail="Vacation balance not found")
    return balance

@api_router.get("/salary-payments/{employee_id}")
async def get_salary_payments(employee_id: str):
    payments = await salary_payments_collection.find(
        {"employee_id": employee_id}
    ).sort("date", -1).limit(12).to_list(12)
    
    formatted_payments = []
    for payment in payments:
        formatted_payments.append({
            "id": payment["id"],
            "amount": payment["amount"],
            "date": payment["date"].isoformat(),
            "status": payment["status"],
            "description": payment["description"]
        })
    
    return {"payments": formatted_payments}

# Statistics endpoint for admin
@api_router.get("/admin/statistics")
async def get_admin_statistics():
    total_employees = await employees_collection.count_documents({})
    total_requests = await hr_requests_collection.count_documents({})
    pending_requests = await hr_requests_collection.count_documents({"status": "Pending Approval"})
    total_policies = await policies_collection.count_documents({})
    
    return {
        "totalEmployees": total_employees,
        "totalRequests": total_requests,
        "pendingRequests": pending_requests,
        "totalPolicies": total_policies
    }

# Include the router in the main app
app.include_router(api_router)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)