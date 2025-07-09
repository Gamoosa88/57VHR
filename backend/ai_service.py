import os
import asyncio
from typing import Dict, Any
from emergentintegrations.llm.chat import LlmChat, UserMessage
from database import employees_collection, vacation_balances_collection, hr_requests_collection, policies_collection, salary_payments_collection

class AIHRAssistant:
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
    
    async def generate_response(self, message: str, employee_id: str, session_id: str) -> Dict[str, Any]:
        """Generate AI response using OpenAI and context from database"""
        
        # Get employee context
        employee = await employees_collection.find_one({"id": employee_id})
        if not employee:
            return {
                "response": "Sorry, I couldn't find your employee information. Please contact HR support.",
                "type": "error"
            }
        
        # Build context with employee data
        context = await self._build_employee_context(employee_id, employee)
        
        # Initialize chat with system message containing HR policies and employee context
        system_message = f"""You are an AI HR Assistant for 1957 Ventures company. You help employees with HR-related questions, policy information, and can assist with form submissions.

Employee Information:
- Name: {employee['name']}
- Grade: {employee['grade']}
- Department: {employee['department']}
- Title: {employee['title']}

Current HR Status:
{context}

HR Policies Summary:
- Grade D employees get 30 vacation days per year
- Grade C and below get 25 vacation days per year
- Sick leave: First 30 days full salary, next 60 days 3/4 salary, next 30 days no salary
- Business travel allowances: 200-400 SAR domestic, 300-600 SAR international based on grade
- Remote work: Maximum 2 days per month, manager approval required
- Working hours: Sunday-Thursday, 8 hours/day, 7:30/8:30 AM to 4:30/5:30 PM

Instructions:
1. Answer HR questions accurately based on the policies
2. Be helpful and professional
3. For specific requests like "request sick leave", guide them to submit a formal request
4. Always reference actual data when available
5. Keep responses concise but informative
6. If you don't know something, be honest and suggest contacting HR directly"""

        try:
            # Create chat instance
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message=system_message
            ).with_model("openai", "gpt-4o").with_max_tokens(500)
            
            # Create user message
            user_message = UserMessage(text=message)
            
            # Get AI response
            ai_response = await chat.send_message(user_message)
            
            # Determine response type based on content
            response_type = self._determine_response_type(message)
            
            return {
                "response": ai_response,
                "type": response_type
            }
            
        except Exception as e:
            print(f"AI Service Error: {str(e)}")
            # Fallback to rule-based responses
            return await self._fallback_response(message, employee_id, context)
    
    async def _build_employee_context(self, employee_id: str, employee: Dict) -> str:
        """Build context string with employee's current HR status"""
        context_parts = []
        
        # Vacation balance
        vacation_balance = await vacation_balances_collection.find_one({"employee_id": employee_id})
        if vacation_balance:
            context_parts.append(f"Vacation Days: {vacation_balance['remaining_days']}/{vacation_balance['total_days']} remaining")
        
        # Recent requests
        recent_requests = await hr_requests_collection.find(
            {"employee_id": employee_id}
        ).sort("submitted_date", -1).limit(3).to_list(3)
        
        if recent_requests:
            context_parts.append("Recent Requests:")
            for req in recent_requests:
                context_parts.append(f"- {req['type']}: {req['status']}")
        
        # Last salary payment
        last_salary = await salary_payments_collection.find_one(
            {"employee_id": employee_id},
            sort=[("date", -1)]
        )
        if last_salary:
            context_parts.append(f"Last Salary: {last_salary['amount']} SAR on {last_salary['date'].strftime('%Y-%m-%d')}")
        
        return "\n".join(context_parts)
    
    def _determine_response_type(self, message: str) -> str:
        """Determine the type of response based on message content"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['request', 'submit', 'apply']):
            return 'action'
        elif any(word in message_lower for word in ['policy', 'rule', 'procedure']):
            return 'policy'
        else:
            return 'query'
    
    async def _fallback_response(self, message: str, employee_id: str, context: str) -> Dict[str, Any]:
        """Fallback rule-based responses when AI fails"""
        message_lower = message.lower()
        
        if 'vacation' in message_lower and 'days' in message_lower:
            vacation_balance = await vacation_balances_collection.find_one({"employee_id": employee_id})
            if vacation_balance:
                return {
                    "response": f"You currently have {vacation_balance['remaining_days']} vacation days remaining out of your annual {vacation_balance['total_days']}-day entitlement.",
                    "type": "query"
                }
        
        if 'sick leave' in message_lower and 'request' in message_lower:
            return {
                "response": "I can help you request sick leave. You'll need to provide a medical certificate. Would you like me to guide you to the sick leave request form?",
                "type": "action"
            }
        
        # Default response
        return {
            "response": "I'm here to help with HR questions about policies, leave requests, salary information, and more. Could you please be more specific about what you'd like to know?",
            "type": "query"
        }