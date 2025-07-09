// Mock data for HR application - based on 1957 Ventures HR policies

export const mockEmployee = {
  id: "EMP001",
  name: "Ahmed Al-Rahman",
  email: "ahmed.alrahman@1957ventures.com",
  title: "Senior Software Engineer",
  department: "Technology",
  grade: "D", // Grade D (higher grade)
  basicSalary: 15000,
  totalSalary: 19500,
  bankAccount: "SA12 3456 7890 1234 5678",
  startDate: "2022-03-15",
  manager: "Sarah Johnson"
};

export const mockDashboardData = {
  vacationDaysLeft: 28, // Grade D gets 30 days, used 2
  pendingRequests: [
    {
      id: "REQ001",
      type: "Business Trip",
      destination: "Dubai",
      status: "Pending Approval",
      submittedDate: "2025-01-10",
      startDate: "2025-01-20"
    },
    {
      id: "REQ002", 
      type: "Expense Reimbursement",
      amount: 450,
      status: "Under Review",
      submittedDate: "2025-01-08"
    }
  ],
  lastSalaryPayment: {
    amount: 19500,
    date: "2025-01-01",
    status: "Paid"
  },
  businessTripStatus: {
    current: "Dubai Business Trip",
    status: "Approved",
    startDate: "2025-01-20",
    endDate: "2025-01-25"
  },
  upcomingEvents: [
    {
      type: "Performance Review",
      date: "2025-01-30"
    },
    {
      type: "Team Meeting", 
      date: "2025-01-15"
    }
  ]
};

export const mockHRRequests = [
  {
    id: "REQ001",
    type: "Vacation Leave",
    startDate: "2024-12-20",
    endDate: "2024-12-30", 
    days: 8,
    status: "Approved",
    submittedDate: "2024-12-01"
  },
  {
    id: "REQ002",
    type: "Sick Leave", 
    startDate: "2024-11-15",
    endDate: "2024-11-17",
    days: 3,
    status: "Approved",
    submittedDate: "2024-11-15",
    medicalCertificate: true
  },
  {
    id: "REQ003",
    type: "Work from Home",
    date: "2025-01-12",
    reason: "Family commitment",
    status: "Approved", 
    submittedDate: "2025-01-08"
  }
];

export const mockPolicies = [
  {
    id: "POL001",
    title: "Annual Leave Policy",
    category: "Leaves",
    content: `Annual Leave entitlements vary by grade:
    
**Grade D and above:** 30 working days per year
**Grade C and below:** 25 working days per year  
**External projects:** 22 working days per year

**Key Rules:**
- Minimum 10 consecutive days must be taken once per year
- Maximum 10 days can be carried forward to next year
- Weekends and public holidays during leave are not counted
- All leave must be approved in advance by authorized person
- Working during leave is prohibited - all system access suspended`,
    tags: ["vacation", "annual", "leave", "entitlement"],
    lastUpdated: "2024-12-01"
  },
  {
    id: "POL002", 
    title: "Sick Leave Policy",
    category: "Leaves",
    content: `Sick leave entitlements as per Saudi Labor Law:

**First 30 days:** Full salary
**Next 60 days:** Three quarters salary  
**Next 30 days:** No salary

**Requirements:**
- Must notify immediate supervisor on first day
- Medical certificate required from approved medical bodies
- Certificates from outside Saudi Arabia must be attested by Saudi Embassy
- No prior approval needed`,
    tags: ["sick", "medical", "leave", "certificate"],
    lastUpdated: "2024-11-15"
  },
  {
    id: "POL003",
    title: "Business Travel Policy", 
    category: "Travel",
    content: `Business travel entitlements by grade:

**Grade A:** First class tickets, 5-star hotels, Junior Suite
**Grade B:** Business class tickets, 5-star hotels, Regular room  
**Grade C:** Economy class tickets, 5-star hotels, Regular room
**Grade D:** Economy class tickets, 4-star hotels, Regular room

**Daily Allowances:**
Inside Kingdom: 200-400 SAR based on grade
Outside Kingdom: 300-600 SAR based on grade

**Accommodation:** Up to 14 days hotel stay provided
**Transportation:** Company provides airport pickup/dropoff`,
    tags: ["travel", "business", "allowance", "accommodation"],
    lastUpdated: "2024-10-20"
  },
  {
    id: "POL004",
    title: "Salary and Compensation",
    category: "Compensation", 
    content: `Salary structure includes:

**Basic Components:**
- Basic salary (determined by grade and experience)
- Housing allowance (25% of basic salary)
- Transportation allowance (varies by grade)

**Additional Benefits:**
- Ramadan bonus (1 month basic salary)
- End of year bonus (1 month basic salary)  
- Medical coverage for employee and family
- Children education allowance (Grades C and above)

**Payment:** Monthly on 15th of each month in Saudi Riyals`,
    tags: ["salary", "compensation", "benefits", "allowance"],
    lastUpdated: "2024-09-10"
  },
  {
    id: "POL005",
    title: "Work Rules and Conduct",
    category: "Conduct",
    content: `Working hours and conduct:

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
- Manager approval required`,
    tags: ["conduct", "dress", "hours", "remote"],
    lastUpdated: "2024-08-15"
  }
];

export const mockChatHistory = [
  {
    id: "chat001",
    message: "How many vacation days do I have left?",
    response: "You currently have 28 vacation days remaining out of your annual 30-day entitlement. You've used 2 days so far this year.",
    timestamp: "2025-01-10T10:30:00Z",
    type: "query"
  },
  {
    id: "chat002", 
    message: "Request a sick leave for tomorrow",
    response: "I can help you request sick leave. Please note that you'll need to provide a medical certificate for the sick leave. Would you like me to submit a sick leave request for January 11th, 2025?",
    timestamp: "2025-01-10T14:15:00Z", 
    type: "action"
  },
  {
    id: "chat003",
    message: "What's the expense policy for meals during business trips?",
    response: "According to the business travel policy, daily allowances cover all expenses including meals. For domestic trips, you receive 200-400 SAR daily based on your grade. For international trips, it's 300-600 SAR daily. These allowances are meant to cover accommodation, meals, transportation, and incidental expenses.",
    timestamp: "2025-01-10T16:45:00Z",
    type: "policy"
  }
];

// Mock form submission responses
export const mockFormSubmissions = {
  success: {
    id: "REQ" + Math.random().toString(36).substr(2, 9),
    status: "Submitted Successfully",
    message: "Your request has been submitted and is pending approval.",
    submittedAt: new Date().toISOString()
  },
  error: {
    status: "Submission Failed", 
    message: "There was an error submitting your request. Please try again."
  }
};