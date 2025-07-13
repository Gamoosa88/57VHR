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
        "name": "Meshal Al Shammari",
        "email": "meshal.alshammari@1957ventures.com",
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
    
    # Create comprehensive policies from 1957 Ventures HR Policy Document
    comprehensive_policies = [
        {
            "id": "POL001",
            "title": "Introduction and Policy Purpose",
            "category": "Introduction",
            "content": """Welcome to the Human Resources Manual of 1957 Ventures Company (الابتكار الجريء لحاضنات ومسرعات الأعمال).

**Policy Purpose / هدف السياسة:**
This manual has been carefully developed to serve as a practical guide for managing our most valuable asset—our people. It reflects our commitment to building a transparent, fair, and professional workplace.

**Objectives:**
- Foster a healthy relationship between the company and its employees
- Clearly outline rights, responsibilities, and expectations of both parties
- Ensure everyone feels supported, informed, and valued in their roles
- Promote a culture of trust, respect, and shared responsibility

**Scope / نطاق السياسة:**
This policy applies to all employees at 1957 Ventures Company (شركة الابتكار الجريء لحاضنات ومسرعات الأعمال) to ensure consistent application of values and standards across the entire company.""",
            "content_ar": """مرحباً بكم في دليل الموارد البشرية لشركة الابتكار الجريء لحاضنات ومسرعات الأعمال.

**هدف السياسة:**
تم إعداد هذا الدليل بعناية ليكون مرجعاً عملياً في إدارة أهم أصول الشركة وهم الموظفون، ويجسد التزامنا بتوفير بيئة عمل تسودها العدالة والشفافية والمهنية.

**الأهداف:**
- تعزيز العلاقة بين الشركة وموظفيها
- توضيح الحقوق والواجبات والمسؤوليات المتبادلة
- ضمان شعور كل موظف بالدعم والتقدير
- ترسيخ ثقافة قائمة على الثقة والاحترام والمسؤولية المشتركة""",
            "tags": ["introduction", "purpose", "scope", "مقدمة", "هدف"],
            "last_updated": datetime(2025, 1, 1),
            "created_at": datetime(2025, 1, 1)
        },
        {
            "id": "POL002",
            "title": "Recruitment Policy - سياسة التوظيف",
            "category": "Recruitment",
            "content": """**Objectives / الأهداف:**
- Attract and select top talent from the job market aligned with strategic needs
- Ensure full compliance with Saudi Labor Law
- Apply principle of equal opportunity with no discrimination based on race, color, gender, age, religion, nationality, marital status, or political beliefs

**Recruitment Criteria / شروط التوظيف:**
1. **Nationality:** Priority to Saudi nationals per Saudization regulations (نطاقات)
2. **Qualifications:** Required academic qualifications and relevant work experience per job description
3. **Age:** Minimum 18 years, not exceeding official retirement age
4. **Medical Fitness:** Valid medical fitness certificate from licensed authority
5. **Interview:** Must pass personal interview and assessments
6. **Criminal Record:** Clear criminal record required
7. **Documents:** All credentials must be original and officially certified

**Probation Period / فترة التجربة:**
- 90 days for all new employees per Saudi Labor Law
- Can be extended once for additional 90 days with written agreement
- Either party may terminate without compensation during probation
- Official holidays and sick leave don't count toward 90 days""",
            "content_ar": """**الأهداف:**
يتناول هذا القسم سياسة التوظيف التي تهدف إلى استقطاب أفضل الكفاءات من سوق العمل بما يتماشى مع احتياجات الشركة الاستراتيجية، مع الالتزام الكامل بأحكام نظام العمل السعودي.

**شروط التوظيف:**
- الجنسية: تُمنح الأولوية للمواطنين السعوديين وفقاً لأنظمة التوطين
- المؤهلات: المؤهلات العلمية والخبرة العملية حسب الوصف الوظيفي
- السن: لا يقل عن 18 عاماً ولا يتجاوز سن التقاعد الرسمي
- اللياقة الطبية: شهادة طبية سارية من جهة معتمدة
- المقابلة الشخصية: اجتياز المقابلة والاختبارات
- السجل الجنائي: سجل خالٍ من السوابق الجنائية""",
            "tags": ["recruitment", "hiring", "probation", "توظيف", "تجربة", "شروط"],
            "last_updated": datetime(2025, 1, 1),
            "created_at": datetime(2025, 1, 1)
        },
        {
            "id": "POL003",
            "title": "Annual Leave Policy - الإجازة السنوية",
            "category": "Leaves",
            "content": """**Annual Leave Balance / رصيد الإجازة السنوية:**

**Grade Entitlements:**
- **Grade D and above:** 30 working days per year
- **Grade C and below:** 25 working days per year  
- **External projects:** 22 working days per year

**Key Rules / القواعد الأساسية:**
- Each employee must take minimum 10 consecutive days once per year
- Maximum 10 days can be carried forward to next year
- New employees (under 6 months) get pro-rata entitlement
- No annual leave for periods of unpaid leave
- Calendar year: January 1 - December 31

**Scheduling / جدولة الإجازة:**
- Must be planned and approved in advance by authorized person
- Shortest leave: Half day
- Taking leave without approval = absence from work (disciplinary action)

**Weekend & Holidays:**
- Weekends and public holidays during annual leave are NOT counted as part of leave period

**During Leave / أثناء الإجازة:**
- All system authorities and access suspended
- Working during leave is PROHIBITED
- Violation subject to disciplinary action per company regulations""",
            "content_ar": """**رصيد الإجازة السنوية:**
- الدرجة الوظيفية D فأعلى: 30 يوم عمل سنوياً
- الدرجة الوظيفية C فأقل: 25 يوم عمل سنوياً
- الوظائف المرتبطة بمشاريع خارجية: 22 يوم عمل سنوياً

**القواعد الأساسية:**
- يجب أخذ 10 أيام متصلة على الأقل مرة واحدة سنوياً
- يمكن ترحيل حد أقصى 10 أيام للسنة التالية
- يتم إيقاف جميع الصلاحيات أثناء الإجازة
- ممنوع العمل أثناء الإجازة السنوية
- العطل الرسمية لا تحتسب ضمن الإجازة السنوية""",
            "tags": ["annual", "leave", "vacation", "إجازة", "سنوية", "عطل"],
            "last_updated": datetime(2025, 1, 1),
            "created_at": datetime(2025, 1, 1)
        },
        {
            "id": "POL004",
            "title": "Sick Leave Policy - الإجازة المرضية",
            "category": "Leaves",
            "content": """**Sick Leave Entitlements (Per Saudi Labor Law):**

**Salary Structure:**
- **First 30 days:** Full pay (بأجر كامل)
- **Next 60 days:** Three quarters pay (ثلاثة أرباع الأجر)
- **Next 30 days:** No pay (بدون أجر)

**Requirements / الشروط:**
- Must notify immediate supervisor on FIRST DAY of absence
- No prior approval required
- Medical reports must be from accredited medical bodies approved by company
- Medical reports from outside Saudi Arabia must be attested by Saudi Embassy

**Total Annual Entitlement:** 120 days maximum per year
- 30 days full salary
- 60 days three-quarters salary  
- 30 days unpaid

**Important Notes:**
- Medical certificate required for all sick leave
- Employee responsibility to provide proper documentation
- Failure to notify supervisor may result in absence being treated as unauthorized""",
            "content_ar": """**استحقاقات الإجازة المرضية حسب نظام العمل السعودي:**

**هيكل الراتب:**
- الثلاثون يوماً الأولى: بأجر كامل
- الستون يوماً التالية: ثلاثة أرباع الأجر
- الثلاثون يوماً التالية: بدون أجر

**الشروط:**
- إخطار الرئيس المباشر في اليوم الأول
- لا يشترط الاعتماد المسبق
- التقارير الطبية من جهات معتمدة
- تقارير من خارج المملكة تحتاج تصديق السفارة السعودية""",
            "tags": ["sick", "medical", "leave", "مرضية", "إجازة", "شهادة"],
            "last_updated": datetime(2025, 1, 1),
            "created_at": datetime(2025, 1, 1)
        },
        {
            "id": "POL005",
            "title": "Maternity Leave - إجازة الأمومة",
            "category": "Leaves",
            "content": """**Maternity Leave Entitlement:**

**Duration:** 10 weeks with full pay
- Can be distributed as employee prefers
- Maximum 4 weeks before expected birth date
- PROHIBITED to work during 6 weeks immediately following birth

**Special Cases:**
- **Sick baby or special needs:** Additional 1 month full pay after maternity leave ends
- **Extension:** 1 month unpaid leave available
- **Nursing time:** 1 hour daily upon return for breastfeeding (counted as working hours)

**Requirements:**
- Expected due date determined by medical certificate from accredited health institution
- Must be attested by company-approved medical facility

**Paternity Leave - إجازة المولود:**
- **Male employees:** 3 working days with pay
- Must be taken within one week of birth date
- Cannot be postponed
- Supporting documents required""",
            "content_ar": """**إجازة الأمومة:**
- المدة: 10 أسابيع بأجر كامل
- توزع حسب رغبة الموظفة
- حد أقصى 4 أسابيع قبل الولادة المتوقعة
- يحظر العمل خلال 6 أسابيع بعد الولادة مباشرة

**الحالات الخاصة:**
- طفل مريض أو ذوي احتياجات خاصة: شهر إضافي بأجر كامل
- التمديد: شهر بدون أجر
- وقت الرضاعة: ساعة يومياً بعد العودة (تحتسب من ساعات العمل)

**إجازة المولود للرجال:**
- 3 أيام عمل بأجر كامل
- خلال أسبوع من تاريخ الولادة""",
            "tags": ["maternity", "paternity", "أمومة", "مولود", "رضاعة"],
            "last_updated": datetime(2025, 1, 1),
            "created_at": datetime(2025, 1, 1)
        },
        {
            "id": "POL006",
            "title": "Other Leave Types - أنواع الإجازات الأخرى",
            "category": "Leaves", 
            "content": """**Hajj Leave - إجازة الحج:**
- Muslim employees: Once during service at company
- 5 working days with pay
- Must be connected with Eid Al-Adha holiday
- Supporting documents required

**Marriage Leave - إجازة الزواج:**
- First marriage only: 5 working days
- Must be taken during marriage period
- Supporting documents required

**Death Leave - إجازة الوفاة:**
- 5 working days for death of first or second degree family member
- Leave starts from date of death
- Supporting documents required
- Special consideration for deaths outside Saudi Arabia

**Iddah Leave - إجازة العدة:**
- Female employee whose husband dies: 130 calendar days with pay
- Starts from date of death per Saudi Labor Law

**Child Companion Leave - إجازة مرافقة الطفل:**
- Female employees: When child (12 years or younger) hospitalized
- Maximum 5 working days per calendar year
- Emergency situations only

**Examination Leave - إجازة الامتحان:**
- Continuing education at recognized institutions in KSA
- Exam day plus previous day for final semester exams
- No summer semester exams
- Non-repeated academic year only
- Requires prior authorization""",
            "content_ar": """**إجازة الحج:**
- للموظف المسلم مرة واحدة طوال الخدمة
- 5 أيام عمل مدفوعة الأجر
- متصلة مع عطلة عيد الأضحى

**إجازة الزواج:**
- للزواج الأول فقط: 5 أيام عمل
- خلال فترة الزواج

**إجازة الوفاة:**
- 5 أيام عمل لوفاة قريب من الدرجة الأولى أو الثانية
- تبدأ من تاريخ الوفاة

**إجازة العدة:**
- الموظفة التي يتوفى زوجها: 130 يوم تقويمي بأجر

**إجازة مرافقة الطفل:**
- للموظفة عند تنويم طفل (12 سنة أو أقل)
- حد أقصى 5 أيام عمل سنوياً""",
            "tags": ["hajj", "marriage", "death", "examination", "حج", "زواج", "وفاة", "امتحان"],
            "last_updated": datetime(2025, 1, 1),
            "created_at": datetime(2025, 1, 1)
        },
        {
            "id": "POL007",
            "title": "Compensation and Benefits - التعويضات والمزايا",
            "category": "Compensation",
            "content": """**Salary Structure / هيكل الراتب:**

**Basic Components:**
- **Basic Salary:** Determined by job grade and experience
- **Housing Allowance:** 25% of basic salary (if housing not provided)
- **Transportation Allowance:** Varies by grade and location
- **Shift Allowance:** For positions requiring shift work
- **Field Allowance:** For field work positions (Grade C and below)

**Annual Bonuses:**
- **Ramadan Bonus:** 1 month basic salary per year
- **End of Year Bonus:** 1 month basic salary per year
- Paid monthly on pro-rata basis
- Not eligible during unpaid leave periods

**Overtime Policy:**
- Applies to Grade C and below
- Prior authorization required
- All holiday work considered overtime
- Must be within approved budget
- Alternative: Lieu leave if no overtime budget

**Merit Increase:**
- Annual performance-based salary increase
- Based on performance rating, employment start date, attendance, warnings
- Maximum increase per salary scale limits

**Payment Schedule:**
- Monthly salary paid on 15th of each Gregorian month in Saudi Riyals
- If 15th falls on holiday, paid on last working day before""",
            "content_ar": """**هيكل الراتب:**
- الراتب الأساسي: حسب الدرجة الوظيفية والخبرة
- بدل السكن: 25% من الراتب الأساسي
- بدل المواصلات: حسب الدرجة والموقع
- بدل المناوبة: للوظائف التي تتطلب مناوبات

**المكافآت السنوية:**
- مكافأة رمضان: راتب شهر أساسي
- مكافأة نهاية السنة: راتب شهر أساسي
- تدفع شهرياً بالنسبة والتناسب

**الأجر الإضافي:**
- للدرجة C فما دون
- موافقة مسبقة مطلوبة
- العمل في العطل يعتبر إضافي""",
            "tags": ["salary", "compensation", "benefits", "راتب", "مزايا", "علاوة", "بدلات"],
            "last_updated": datetime(2025, 1, 1),
            "created_at": datetime(2025, 1, 1)
        },
        {
            "id": "POL008",
            "title": "Business Travel Policy - سياسة الانتداب",
            "category": "Travel",
            "content": """**Travel Entitlements by Grade:**

**Grade A:** First class tickets, 5-star hotels, Junior Suite
**Grade B:** Business class tickets, 5-star hotels, Regular room  
**Grade C:** Economy class tickets, 5-star hotels, Regular room
**Grade D:** Economy class tickets, 4-star hotels, Regular room

**Daily Allowances:**
**Assignment requiring overnight stay:**
- Inside Kingdom: 200-400 SAR based on grade
- Outside Kingdom: 300-600 SAR based on grade

**Assignment not requiring overnight stay:**
- Minimum 80km distance from work area
- Covers meals, transportation, miscellaneous expenses

**Travel Accommodations:**
- Hotel accommodation as per policy (up to 14 days)
- Team accommodation upgraded to highest grade member's level
- Direct routing flights provided
- Company handles airport pickup/dropoff

**Special Cases:**
- No personal vehicle areas: 0.50 SAR per kilometer instead of air ticket
- Car rental: Daily rate plus actual excess kilometers and fuel costs
- Entry visas: Company covers for assignment period
- International assignments: No cash compensation for air tickets
- Domestic/GCC: Cash compensation possible for air tickets""",
            "content_ar": """**استحقاقات السفر حسب الدرجة:**
- الدرجة A: درجة أولى، فندق 5 نجوم، جناح
- الدرجة B: درجة رجال أعمال، فندق 5 نجوم
- الدرجة C: درجة سياحية، فندق 5 نجوم  
- الدرجة D: درجة سياحية، فندق 4 نجوم

**البدل اليومي:**
**الانتداب مع مبيت:**
- داخل المملكة: 200-400 ريال حسب الدرجة
- خارج المملكة: 300-600 ريال حسب الدرجة

**الانتداب بدون مبيت:**
- مسافة لا تقل عن 80 كيلو
- يغطي الإعاشة والمواصلات والمصروفات النثرية""",
            "tags": ["travel", "business", "allowance", "انتداب", "سفر", "بدل"],
            "last_updated": datetime(2025, 1, 1),
            "created_at": datetime(2025, 1, 1)
        },
        {
            "id": "POL009",
            "title": "Work Rules and Conduct - قواعد العمل والسلوك",
            "category": "Conduct",
            "content": """**Working Hours / ساعات العمل:**
- **Working Days:** 5 days per week (Sunday to Thursday)
- **Daily Hours:** 8 actual hours per day, 40 hours per week
- **Official Hours:** 7:30/8:30 AM to 4:30/5:30 PM (including lunch hour)
- Attendance recording through company approved system required

**Remote Work Policy / العمل عن بعد:**
- Maximum 2 days per month allowed
- Single request: Maximum 2 consecutive working days
- Cannot be beginning or end of week
- Manager approval required
- Maximum 25% of company employees working remotely
- May not be summoned to office during remote work period (except urgent needs)

**Dress Code / قواعد الزي:**
**Men:** Saudi national dress, formal/sports shoes, shirt with tie, jeans acceptable
**Women:** Conservative covering clothing, loose abaya, calm colors, Islamic hijab required, low-heeled shoes, professional appearance

**Employee ID Card / بطاقة الموظف:**
- Must carry and display clearly during work
- Personal card - cannot be loaned
- No modifications allowed
- Must return upon service termination
- Report loss immediately to Security & Safety

**Prohibited Activities:**
- Working for other parties without approval
- Working for competitors
- Smoking in workplace or building vicinity
- Accepting gifts, bribes, or privileges
- Disclosing confidential information
- Media representation of company on social media""",
            "content_ar": """**ساعات العمل:**
- 5 أيام أسبوعياً (الأحد للخميس)
- 8 ساعات فعلية يومياً، 40 ساعة أسبوعياً
- الدوام الرسمي: 7:30-8:30 صباحاً إلى 4:30-5:30 مساءً

**العمل عن بعد:**
- حد أقصى يومين شهرياً
- لا يتجاوز الطلب الواحد يومين متتاليين
- ليس بداية أو نهاية الأسبوع
- موافقة المدير مطلوبة

**قواعد الزي:**
- للرجال: الثوب السعودي، أحذية رسمية، قميص مع ربطة عنق
- للنساء: ملابس ساترة محتشمة، عباءة فضفاضة، حجاب إسلامي""",
            "tags": ["conduct", "dress", "hours", "remote", "سلوك", "زي", "ساعات", "بعد"],
            "last_updated": datetime(2025, 1, 1),
            "created_at": datetime(2025, 1, 1)
        },
        {
            "id": "POL010",
            "title": "End of Service Benefits - مكافأة نهاية الخدمة",
            "category": "End of Service",
            "content": """**End of Service Benefit Calculation:**

**Salary Components Included:**
- Basic salary
- Housing allowance
- Transportation allowance  
- Ramadan bonus
- End of year bonus
- Shift allowance
- Cash handling allowance
(Must be paid continuously until last month of service)

**Calculation Method:**
- **First 5 years:** Half month salary for each year
- **After 5 years:** Full month salary for each year

**Full Benefit Payment Cases:**
- Contract expiration and non-renewal (both parties)
- Termination by company (except Article 80 cases)
- Resignation due to force majeure
- Female resignation within 6 months of marriage or 3 months of childbirth

**Resignation Cases:**
- **Less than 2 years:** No benefit
- **2-5 years:** 1/3 of regular benefit per year
- **5-10 years:** 2/3 of regular benefit per year  
- **10+ years:** Full benefit per year

**Human Cases Compensation:**
- Upon death or serious illness leading to permanent disability
- Write-off of outstanding obligations
- Medical coverage extended 1 year for family
- Compensation based on service length (5-30 months basic salary)

**Notice Period:**
- As specified in employment contract
- Annual leave can cover part of notice period (with approval)
- Employee must pay for unworked notice period (unless exempted)""",
            "content_ar": """**احتساب مكافأة نهاية الخدمة:**

**العناصر المشمولة:**
- الراتب الأساسي
- بدل السكن
- بدل النقل
- مكافأة رمضان
- مكافأة نهاية السنة
- بدل المناوبة

**طريقة الحساب:**
- الخمس سنوات الأولى: نصف راتب شهر لكل سنة
- أكثر من خمس سنوات: راتب شهر كامل لكل سنة

**حالات الاستحقاق الكامل:**
- انتهاء العقد وعدم التجديد
- إنهاء من الشركة (غير حالات المادة 80)
- استقالة بسبب قوة قاهرة
- استقالة الموظفة خلال 6 أشهر من الزواج أو 3 أشهر من الولادة""",
            "tags": ["end", "service", "benefit", "نهاية", "خدمة", "مكافأة", "تقاعد"],
            "last_updated": datetime(2025, 1, 1),
            "created_at": datetime(2025, 1, 1)
        },
        {
            "id": "POL011",
            "title": "Performance Management - إدارة الأداء",
            "category": "Performance",
            "content": """**Performance Management System:**

**Balanced Scorecard Method:**
Four key areas for individual and group goals:
1. Financial Performance
2. Customer Service  
3. Processes
4. People Development

**Performance Ratings:**
- **Exceptional Performer (5):** Exceeds all indicators, role model performance
- **Outstanding Performer (4):** Consistently achieves goals, stronger than peers
- **Strong Performer (3):** Meets expectations, contributes to success
- **Average Performer (2):** Inconsistent performance, needs improvement (PIP required)
- **Poor Performer (1):** Fails minimum requirements, poor performance (PIP required)

**Performance Cycle:**
- **Performance Year:** January 1 - December 31
- **Goal Setting:** January (KPIs must be SMART goals)
- **Mid-Year Review:** Formal review by direct manager
- **Year-End Evaluation:** December formal review and discussion

**Eligibility Criteria:**
- Employees joining after September 30: Not evaluated
- Minimum 3 months continuous service required
- Transfer employees: Evaluated by current manager

**Natural Distribution Curve (NDC):**
- Applied across company, varies by department performance
- No specific mandatory percentage for Strong Performer rating
- Final evaluation considers both financial and non-financial goals

**Poor Performance Policy:**
- Progressive steps: First warning → Second warning → Third warning → Termination
- Performance Improvement Plan (PIP) for Average/Poor performers
- Clear action plans with 3-month maximum timeframes""",
            "content_ar": """**نظام إدارة الأداء:**

**بطاقة الأداء المتوازن:**
أربعة مناطق رئيسية للأهداف:
1. الأداء المالي
2. خدمة العملاء  
3. العمليات
4. تطوير الموظفين

**تقييمات الأداء:**
- الأداء الاستثنائي (5): يتجاوز جميع المؤشرات
- الأداء المتميز (4): يحقق الأهداف باستمرار
- الأداء القوي (3): يلبي التوقعات
- الأداء المتوسط (2): أداء متقطع، يحتاج تحسين
- الأداء الضعيف (1): لا يلبي الحد الأدنى

**دورة الأداء:**
- سنة الأداء: 1 يناير - 31 ديسمبر
- وضع الأهداف: يناير
- مراجعة منتصف العام: مراجعة رسمية
- تقييم نهاية العام: ديسمبر""",
            "tags": ["performance", "management", "evaluation", "أداء", "تقييم", "إدارة"],
            "last_updated": datetime(2025, 1, 1),
            "created_at": datetime(2025, 1, 1)
        },
        {
            "id": "POL012",
            "title": "Administrative Services - الخدمات الإدارية",
            "category": "Administrative",
            "content": """**Equipment Usage / استخدام الأجهزة:**

**Phone/Fax:**
- Official business purposes only
- Personal use allowed only in emergencies during breaks (employee pays for calls within KSA)
- International calls for specific jobs with prior authorization

**Computer/Laptops:**
- Provided based on computer equipment distribution policy
- Desktop and laptop allocation per business needs

**Mobile Devices:**
- Grades [specific range]: Provided devices for email access
- Others: Available with authorized person approval

**Internet Service:**
- Provided for Grades [specific range]
- Others: Available with prior authorization

**Business Call Compensation:**
- Maximum 500 SAR per bill for business calls
- Phone must be registered in employee's name
- Only one phone number per employee for company calls
- Requires authorized person approval

**Work Permit (Iqama) for Non-Saudis:**
- Company provides residence permits (new/renewal) at company expense
- Work permits for non-Saudis
- Family sponsorship costs (wife/children under 18) - once only with approval

**Exit/Re-entry Visas:**
- Company completes procedures and bears costs once per year
- Multiple/single visas based on grade level
- Family members included per grade entitlements

**Final Exit/Transfer of Sponsorship:**
- 60-day grace period for transfer procedures with company approval
- Return tickets for final exit (employee and eligible family)
- Luggage transfer costs covered for specific grades (up to 20-foot container or specified SAR amount)""",
            "content_ar": """**استخدام الأجهزة:**

**الهاتف/الفاكس:**
- لأغراض العمل الرسمي فقط
- الاستخدام الشخصي في الطوارئ فقط (الموظف يدفع للمكالمات داخل المملكة)

**الحاسوب:**
- يوفر حسب سياسة توزيع أجهزة الحاسب الآلي

**الأجهزة المحمولة:**
- للدرجات المحددة: أجهزة للدخول للبريد الإلكتروني
- الآخرون: بموافقة مسبقة

**التعويض عن مكالمات العمل:**
- حد أقصى 500 ريال لكل فاتورة
- الهاتف مسجل باسم الموظف
- رقم هاتف واحد فقط لمكالمات الشركة""",
            "tags": ["administrative", "services", "equipment", "إدارية", "خدمات", "أجهزة"],
            "last_updated": datetime(2025, 1, 1),
            "created_at": datetime(2025, 1, 1)
        },
        # Keep some existing basic policies for compatibility
        {
            "id": "POL013",
            "title": "Children Education Allowance",
            "category": "Benefits",
            "content": """**Children Education Benefits:**

**Grade Eligibility:** Grade B and above
**Coverage:** Actual cost for children inside and outside Saudi Arabia
**Age Range:** 5-18 years old
**Number of Children:** Maximum 3 children per family

**Maximum Annual Costs:**
- Grade B: Specific amount per child
- Grade A: Higher amount per child

**Included Expenses:**
- Registration fees
- Non-refundable deposits
- Books and materials
- Transportation
- Uniforms  
- VAT included
- Supporting documents required

**Nursery Allowance (Alternative):**
- Female employees: 500 SAR per child per month
- Maximum 1,000 SAR per month total
- Children under 6 years (calculated in November)
- Choice between nursery allowance OR education allowance for children 5-6 years (Grade B and above)

**Conditions:**
- Pro-rata calculation if child completes age limit during year
- Pro-rata for new employees after probation
- Deduction for resignation during semester
- No deduction if company terminates during semester""",
            "content_ar": """**بدل تعليم الأطفال:**

**الاستحقاق:** الدرجة B فأعلى
**التغطية:** التكلفة الفعلية داخل وخارج المملكة
**الأعمار:** 5-18 سنة
**عدد الأطفال:** حد أقصى 3 أطفال

**المصاريف المشمولة:**
- رسوم التسجيل
- مبلغ التأمين غير المسترد
- الكتب والمواد
- المواصلات
- الزي المدرسي
- ضريبة القيمة المضافة

**بدل الحضانة (البديل):**
- للموظفات: 500 ريال شهرياً للطفل
- حد أقصى 1000 ريال شهرياً
- للأطفال تحت 6 سنوات""",
            "tags": ["education", "children", "allowance", "تعليم", "أطفال", "بدل"],
            "last_updated": datetime(2025, 1, 1),
            "created_at": datetime(2025, 1, 1)
        }
    ]
    await policies_collection.insert_many(comprehensive_policies)
    
    print("✅ Database initialized with sample data")