from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timedelta

# Database connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Collections
employees_collection = db.employees
hr_requests_collection = db.hr_requests
policies_collection = db.policies
chat_messages_collection = db.chat_messages
vacation_balances_collection = db.vacation_balances
salary_payments_collection = db.salary_payments
sessions_collection = db.sessions

async def init_database():
    """Initialize database with sample data"""
    
    # Check if we already have data
    employee_count = await employees_collection.count_documents({})
    if employee_count > 0:
        return  # Database already initialized
    
    # Create sample employee
    sample_employee = {
        "id": "EMP001",
        "name": "Basel",
        "email": "basel@1957ventures.com",
        "title": "Senior Software Engineer",
        "department": "Technology",
        "grade": "D",
        "basic_salary": 15000.0,
        "total_salary": 19500.0,
        "bank_account": "SA12 3456 7890 1234 5678",
        "start_date": "2022-03-15",
        "manager": "Sarah Johnson",
        "created_at": datetime.utcnow()
    }
    await employees_collection.insert_one(sample_employee)
    
    # Create vacation balance
    vacation_balance = {
        "employee_id": "EMP001",
        "total_days": 30,  # Grade D gets 30 days
        "used_days": 2,
        "remaining_days": 28,
        "year": 2025
    }
    await vacation_balances_collection.insert_one(vacation_balance)
    
    # Create sample salary payment
    salary_payment = {
        "id": "PAY001",
        "employee_id": "EMP001",
        "amount": 19500.0,
        "date": datetime(2025, 1, 1),
        "status": "Paid",
        "description": "Monthly Salary"
    }
    await salary_payments_collection.insert_one(salary_payment)
    
    # Create sample HR requests
    sample_requests = [
        {
            "id": "REQ001",
            "employee_id": "EMP001",
            "type": "Business Trip",
            "destination": "Dubai",
            "status": "Pending Approval",
            "submitted_date": datetime(2025, 1, 10),
            "departure_date": "2025-01-20",
            "return_date": "2025-01-25",
            "business_purpose": "Client meeting and project review",
            "duration": 5
        },
        {
            "id": "REQ002",
            "employee_id": "EMP001",
            "type": "Expense Reimbursement",
            "amount": 450.0,
            "category": "meals",
            "description": "Client dinner during business trip",
            "status": "Under Review",
            "submitted_date": datetime(2025, 1, 8)
        },
        {
            "id": "REQ003",
            "employee_id": "EMP001",
            "type": "Vacation Leave",
            "start_date": "2024-12-20",
            "end_date": "2024-12-30",
            "days": 8,
            "reason": "Family vacation",
            "status": "Approved",
            "submitted_date": datetime(2024, 12, 1),
            "approved_date": datetime(2024, 12, 2),
            "approved_by": "Sarah Johnson"
        }
    ]
    await hr_requests_collection.insert_many(sample_requests)
    
    # Create sample policies
    sample_policies = [
        {
            "id": "POL001",
            "title": "Annual Leave Policy",
            "category": "Leaves",
            "content": """Annual Leave entitlements vary by grade:
    
**Grade D and above:** 30 working days per year
**Grade C and below:** 25 working days per year  
**External projects:** 22 working days per year

**Key Rules:**
- Minimum 10 consecutive days must be taken once per year
- Maximum 10 days can be carried forward to next year
- Weekends and public holidays during leave are not counted
- All leave must be approved in advance by authorized person
- Working during leave is prohibited - all system access suspended""",
            "tags": ["vacation", "annual", "leave", "entitlement"],
            "last_updated": datetime(2024, 12, 1),
            "created_at": datetime(2024, 12, 1)
        },
        {
            "id": "POL002",
            "title": "Sick Leave Policy",
            "category": "Leaves",
            "content": """Sick leave entitlements as per Saudi Labor Law:

**First 30 days:** Full salary
**Next 60 days:** Three quarters salary  
**Next 30 days:** No salary

**Requirements:**
- Must notify immediate supervisor on first day
- Medical certificate required from approved medical bodies
- Certificates from outside Saudi Arabia must be attested by Saudi Embassy
- No prior approval needed""",
            "tags": ["sick", "medical", "leave", "certificate"],
            "last_updated": datetime(2024, 11, 15),
            "created_at": datetime(2024, 11, 15)
        },
        {
            "id": "POL003",
            "title": "Business Travel Policy",
            "category": "Travel",
            "content": """Business travel entitlements by grade:

**Grade A:** First class tickets, 5-star hotels, Junior Suite
**Grade B:** Business class tickets, 5-star hotels, Regular room  
**Grade C:** Economy class tickets, 5-star hotels, Regular room
**Grade D:** Economy class tickets, 4-star hotels, Regular room

**Daily Allowances:**
Inside Kingdom: 200-400 SAR based on grade
Outside Kingdom: 300-600 SAR based on grade

**Accommodation:** Up to 14 days hotel stay provided
**Transportation:** Company provides airport pickup/dropoff""",
            "tags": ["travel", "business", "allowance", "accommodation"],
            "last_updated": datetime(2024, 10, 20),
            "created_at": datetime(2024, 10, 20)
        },
        {
            "id": "POL004",
            "title": "Salary and Compensation",
            "category": "Compensation",
            "content": """Salary structure includes:

**Basic Components:**
- Basic salary (determined by grade and experience)
- Housing allowance (25% of basic salary)
- Transportation allowance (varies by grade)

**Additional Benefits:**
- Ramadan bonus (1 month basic salary)
- End of year bonus (1 month basic salary)  
- Medical coverage for employee and family
- Children education allowance (Grades C and above)

**Payment:** Monthly on 15th of each month in Saudi Riyals""",
            "tags": ["salary", "compensation", "benefits", "allowance"],
            "last_updated": datetime(2024, 9, 10),
            "created_at": datetime(2024, 9, 10)
        },
        {
            "id": "POL005",
            "title": "Work Rules and Conduct",
            "category": "Conduct",
            "content": """Working hours and conduct:

**Working Hours:**
- 5 days per week (Sunday to Thursday)
- 8 hours per day, 40 hours per week
- Official hours: 7:30/8:30 AM to 4:30/5:30 PM

**Dress Code:**
- Professional attire required
- Saudi national dress acceptable for men
- Conservative dress for women with hijab
- Low-heeled shoes recommended

**Remote Work:** 
- Maximum 2 days per month allowed
- Cannot be start/end of week
- Manager approval required""",
            "tags": ["conduct", "dress", "hours", "remote"],
            "last_updated": datetime(2024, 8, 15),
            "created_at": datetime(2024, 8, 15)
        }
    ]
    await policies_collection.insert_many(sample_policies)
    
    print("✅ Database initialized with sample data")