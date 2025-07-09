import requests
import json
import unittest
import uuid
from datetime import datetime, timedelta

# Get the backend URL from the frontend .env file
BACKEND_URL = "https://161b1335-227a-4505-afe4-6876d8d902b5.preview.emergentagent.com/api"
EMPLOYEE_ID = "EMP001"

class HRHubBackendTests(unittest.TestCase):
    def setUp(self):
        self.api_url = BACKEND_URL
        self.employee_id = EMPLOYEE_ID
        self.session_id = str(uuid.uuid4())  # Generate a unique session ID for chat tests

    def test_health_check(self):
        """Test the API health check endpoint"""
        response = requests.get(f"{self.api_url}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "1957 Ventures HR Hub API")
        self.assertEqual(data["status"], "running")
        print("✅ Health check endpoint working")

    # Employee Management Tests
    def test_get_employee(self):
        """Test getting a specific employee"""
        response = requests.get(f"{self.api_url}/employees/{self.employee_id}")
        self.assertEqual(response.status_code, 200)
        employee = response.json()
        self.assertEqual(employee["id"], self.employee_id)
        self.assertEqual(employee["name"], "Ahmed Al-Rahman")
        self.assertEqual(employee["department"], "Technology")
        print(f"✅ Get employee endpoint working - Retrieved {employee['name']}")

    def test_get_all_employees(self):
        """Test getting all employees"""
        response = requests.get(f"{self.api_url}/employees")
        self.assertEqual(response.status_code, 200)
        employees = response.json()
        self.assertIsInstance(employees, list)
        self.assertGreater(len(employees), 0)
        print(f"✅ Get all employees endpoint working - Retrieved {len(employees)} employees")

    # Dashboard Tests
    def test_get_dashboard_data(self):
        """Test getting dashboard data for an employee"""
        response = requests.get(f"{self.api_url}/dashboard/{self.employee_id}")
        self.assertEqual(response.status_code, 200)
        dashboard = response.json()
        
        # Verify dashboard structure
        self.assertIn("vacationDaysLeft", dashboard)
        self.assertIn("pendingRequests", dashboard)
        self.assertIn("lastSalaryPayment", dashboard)
        self.assertIn("businessTripStatus", dashboard)
        self.assertIn("upcomingEvents", dashboard)
        
        # Verify data types
        self.assertIsInstance(dashboard["vacationDaysLeft"], int)
        self.assertIsInstance(dashboard["pendingRequests"], list)
        self.assertIsInstance(dashboard["lastSalaryPayment"], dict)
        self.assertIsInstance(dashboard["businessTripStatus"], dict)
        self.assertIsInstance(dashboard["upcomingEvents"], list)
        
        print(f"✅ Dashboard endpoint working - Vacation days left: {dashboard['vacationDaysLeft']}")

    # HR Requests Tests
    def test_create_and_get_hr_request(self):
        """Test creating a new HR request and retrieving it"""
        # Create a new vacation request
        today = datetime.now()
        start_date = (today + timedelta(days=10)).strftime("%Y-%m-%d")
        end_date = (today + timedelta(days=15)).strftime("%Y-%m-%d")
        
        request_data = {
            "employee_id": self.employee_id,
            "type": "Vacation Leave",
            "start_date": start_date,
            "end_date": end_date,
            "reason": "Family vacation"
        }
        
        # Create request
        create_response = requests.post(
            f"{self.api_url}/hr-requests", 
            json=request_data
        )
        self.assertEqual(create_response.status_code, 200)
        created_request = create_response.json()
        self.assertEqual(created_request["employee_id"], self.employee_id)
        self.assertEqual(created_request["type"], "Vacation Leave")
        self.assertEqual(created_request["status"], "Pending Approval")
        
        # Get employee's HR requests
        get_response = requests.get(f"{self.api_url}/hr-requests/{self.employee_id}")
        self.assertEqual(get_response.status_code, 200)
        requests_list = get_response.json()
        self.assertIsInstance(requests_list, list)
        
        # Verify our new request is in the list
        request_ids = [req["id"] for req in requests_list]
        self.assertIn(created_request["id"], request_ids)
        
        print(f"✅ HR request creation and retrieval working - Created request ID: {created_request['id']}")
        
        return created_request["id"]  # Return ID for update test

    def test_update_hr_request_status(self):
        """Test updating an HR request status"""
        # First create a request
        request_id = self.test_create_and_get_hr_request()
        
        # Update the status
        update_response = requests.put(
            f"{self.api_url}/hr-requests/{request_id}/status",
            params={"status": "Approved", "approved_by": "Test Manager"}
        )
        self.assertEqual(update_response.status_code, 200)
        update_result = update_response.json()
        self.assertEqual(update_result["message"], "Request status updated successfully")
        
        # Verify the update
        get_response = requests.get(f"{self.api_url}/hr-requests/{self.employee_id}")
        self.assertEqual(get_response.status_code, 200)
        requests_list = get_response.json()
        
        # Find our updated request
        updated_request = next((req for req in requests_list if req["id"] == request_id), None)
        self.assertIsNotNone(updated_request)
        self.assertEqual(updated_request["status"], "Approved")
        self.assertIsNotNone(updated_request["approved_date"])
        self.assertEqual(updated_request["approved_by"], "Test Manager")
        
        print(f"✅ HR request status update working - Updated request ID: {request_id}")

    # Policy Management Tests
    def test_get_all_policies(self):
        """Test getting all policies"""
        response = requests.get(f"{self.api_url}/policies")
        self.assertEqual(response.status_code, 200)
        policies = response.json()
        self.assertIsInstance(policies, list)
        self.assertGreater(len(policies), 0)
        print(f"✅ Get all policies endpoint working - Retrieved {len(policies)} policies")

    def test_get_policy_by_id(self):
        """Test getting a specific policy by ID"""
        # First get all policies to find an ID
        all_response = requests.get(f"{self.api_url}/policies")
        self.assertEqual(all_response.status_code, 200)
        policies = all_response.json()
        
        if policies:
            policy_id = policies[0]["id"]
            
            # Get specific policy
            response = requests.get(f"{self.api_url}/policies/{policy_id}")
            self.assertEqual(response.status_code, 200)
            policy = response.json()
            self.assertEqual(policy["id"], policy_id)
            print(f"✅ Get policy by ID endpoint working - Retrieved policy: {policy['title']}")
        else:
            self.fail("No policies found to test get_policy_by_id")

    def test_get_policies_with_filters(self):
        """Test getting policies with category and search filters"""
        # Get policy categories first
        categories_response = requests.get(f"{self.api_url}/policies/categories")
        self.assertEqual(categories_response.status_code, 200)
        categories = categories_response.json()["categories"]
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)
        
        # Test filtering by category
        if categories:
            category = categories[0]
            response = requests.get(f"{self.api_url}/policies", params={"category": category})
            self.assertEqual(response.status_code, 200)
            filtered_policies = response.json()
            self.assertIsInstance(filtered_policies, list)
            
            # Verify all returned policies have the correct category
            for policy in filtered_policies:
                self.assertEqual(policy["category"], category)
            
            print(f"✅ Policy category filter working - Retrieved {len(filtered_policies)} policies in category '{category}'")
        
        # Test search functionality
        search_term = "leave"
        search_response = requests.get(f"{self.api_url}/policies", params={"search": search_term})
        self.assertEqual(search_response.status_code, 200)
        search_results = search_response.json()
        self.assertIsInstance(search_results, list)
        
        print(f"✅ Policy search filter working - Found {len(search_results)} policies matching '{search_term}'")

    # AI Chat Assistant Tests
    def test_chat_message_and_history(self):
        """Test sending a chat message and retrieving chat history"""
        # Send a chat message
        message_data = {
            "employee_id": self.employee_id,
            "session_id": self.session_id,
            "message": "What is the vacation policy?"
        }
        
        send_response = requests.post(
            f"{self.api_url}/chat/message", 
            json=message_data
        )
        self.assertEqual(send_response.status_code, 200)
        chat_result = send_response.json()
        
        # Verify response structure
        self.assertIn("id", chat_result)
        self.assertIn("message", chat_result)
        self.assertIn("response", chat_result)
        self.assertIn("type", chat_result)
        self.assertIn("timestamp", chat_result)
        
        # Verify the message was saved correctly
        self.assertEqual(chat_result["message"], message_data["message"])
        
        # Get chat history
        history_response = requests.get(
            f"{self.api_url}/chat/history/{self.employee_id}",
            params={"session_id": self.session_id}
        )
        self.assertEqual(history_response.status_code, 200)
        history = history_response.json()["messages"]
        self.assertIsInstance(history, list)
        
        # Verify our message is in the history
        message_ids = [msg["id"] for msg in history]
        self.assertIn(chat_result["id"], message_ids)
        
        print(f"✅ Chat message and history endpoints working - Message ID: {chat_result['id']}")
        print(f"✅ AI response: '{chat_result['response'][:50]}...'")

    # Additional Features Tests
    def test_vacation_balance(self):
        """Test getting vacation balance for an employee"""
        response = requests.get(f"{self.api_url}/vacation-balance/{self.employee_id}")
        self.assertEqual(response.status_code, 200)
        balance = response.json()
        
        # Verify balance structure
        self.assertIn("employee_id", balance)
        self.assertIn("total_days", balance)
        self.assertIn("used_days", balance)
        self.assertIn("remaining_days", balance)
        self.assertIn("year", balance)
        
        # Verify data
        self.assertEqual(balance["employee_id"], self.employee_id)
        self.assertEqual(balance["total_days"] - balance["used_days"], balance["remaining_days"])
        
        print(f"✅ Vacation balance endpoint working - {balance['remaining_days']} days remaining")

    def test_salary_payments(self):
        """Test getting salary payment history for an employee"""
        response = requests.get(f"{self.api_url}/salary-payments/{self.employee_id}")
        self.assertEqual(response.status_code, 200)
        payments = response.json()["payments"]
        self.assertIsInstance(payments, list)
        
        if payments:
            # Verify payment structure
            payment = payments[0]
            self.assertIn("id", payment)
            self.assertIn("amount", payment)
            self.assertIn("date", payment)
            self.assertIn("status", payment)
            self.assertIn("description", payment)
            
            print(f"✅ Salary payments endpoint working - Retrieved {len(payments)} payments")
        else:
            print("⚠️ No salary payments found for testing")

    def test_admin_statistics(self):
        """Test getting admin statistics"""
        response = requests.get(f"{self.api_url}/admin/statistics")
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        
        # Verify stats structure
        self.assertIn("totalEmployees", stats)
        self.assertIn("totalRequests", stats)
        self.assertIn("pendingRequests", stats)
        self.assertIn("totalPolicies", stats)
        
        # Verify data types
        self.assertIsInstance(stats["totalEmployees"], int)
        self.assertIsInstance(stats["totalRequests"], int)
        self.assertIsInstance(stats["pendingRequests"], int)
        self.assertIsInstance(stats["totalPolicies"], int)
        
        print(f"✅ Admin statistics endpoint working - {stats['totalEmployees']} employees, {stats['totalRequests']} requests")

if __name__ == "__main__":
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add tests in a specific order
    test_suite.addTest(HRHubBackendTests('test_health_check'))
    
    # Employee Management
    test_suite.addTest(HRHubBackendTests('test_get_employee'))
    test_suite.addTest(HRHubBackendTests('test_get_all_employees'))
    
    # Dashboard
    test_suite.addTest(HRHubBackendTests('test_get_dashboard_data'))
    
    # HR Requests
    test_suite.addTest(HRHubBackendTests('test_create_and_get_hr_request'))
    test_suite.addTest(HRHubBackendTests('test_update_hr_request_status'))
    
    # Policy Management
    test_suite.addTest(HRHubBackendTests('test_get_all_policies'))
    test_suite.addTest(HRHubBackendTests('test_get_policy_by_id'))
    test_suite.addTest(HRHubBackendTests('test_get_policies_with_filters'))
    
    # AI Chat Assistant
    test_suite.addTest(HRHubBackendTests('test_chat_message_and_history'))
    
    # Additional Features
    test_suite.addTest(HRHubBackendTests('test_vacation_balance'))
    test_suite.addTest(HRHubBackendTests('test_salary_payments'))
    test_suite.addTest(HRHubBackendTests('test_admin_statistics'))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)