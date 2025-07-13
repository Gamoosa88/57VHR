import os
import asyncio
from typing import Dict, Any
import openai
from database import employees_collection, vacation_balances_collection, hr_requests_collection, policies_collection, salary_payments_collection

class AIHRAssistant:
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        # Initialize OpenAI client
        openai.api_key = self.api_key
        self.custom_gpt_id = "g-685d53e450208191992ef69c0eb2d63c-1957v-hr-assistant"
    
    async def generate_response(self, message: str, employee_id: str, session_id: str) -> Dict[str, Any]:
        """Generate AI response using custom GPT and context from database"""
        
        # Get employee context
        employee = await employees_collection.find_one({"id": employee_id})
        if not employee:
            return {
                "response": "Sorry, I couldn't find your employee information. Please contact HR support.",
                "type": "error"
            }
        
        # Build context with employee data
        context = await self._build_employee_context(employee_id, employee)
        
        # Check if this is a policy-related question
        if self._is_policy_question(message):
            try:
                # Use custom GPT for policy questions
                response = await self._query_custom_gpt(message, employee, context)
                return {
                    "response": response,
                    "type": "policy"
                }
            except Exception as e:
                print(f"Custom GPT Error: {str(e)}")
                # Fallback to policy retrieval from database
                return await self._handle_policy_fallback(message, employee_id, context)
        else:
            # Use regular OpenAI for non-policy questions
            return await self._handle_regular_query(message, employee, context, session_id)
    
    def _is_policy_question(self, message: str) -> bool:
        """Check if the message is asking about policies"""
        policy_keywords = [
            'policy', 'policies', 'rule', 'rules', 'procedure', 'procedures',
            'leave policy', 'vacation policy', 'sick leave policy', 'travel policy',
            'compensation policy', 'salary policy', 'work rules', 'conduct',
            'what is the policy', 'policy on', 'company policy', 'hr policy'
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in policy_keywords)
    
    async def _query_custom_gpt(self, message: str, employee: Dict, context: str) -> str:
        """Query the custom GPT for policy-related questions"""
        
        # Create a thread for the conversation
        thread = openai.beta.threads.create()
        
        # Add employee context to the message
        enhanced_message = f"""
Employee Information:
- Name: {employee['name']}
- Grade: {employee['grade']}
- Department: {employee['department']}
- Title: {employee['title']}

Current HR Status:
{context}

Question: {message}
"""
        
        # Add the message to the thread
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=enhanced_message
        )
        
        # Run the assistant
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.custom_gpt_id
        )
        
        # Wait for completion
        while run.status in ['queued', 'in_progress', 'cancelling']:
            await asyncio.sleep(1)
            run = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
        
        if run.status == 'completed':
            # Get the messages
            messages = openai.beta.threads.messages.list(
                thread_id=thread.id
            )
            
            # Return the assistant's response
            for message in messages.data:
                if message.role == "assistant":
                    return message.content[0].text.value
            
            return "I couldn't get a proper response from the policy assistant. Please try again or contact HR directly."
        else:
            raise Exception(f"Assistant run failed with status: {run.status}")
    
    async def _handle_regular_query(self, message: str, employee: Dict, context: str, session_id: str) -> Dict[str, Any]:
        """Handle non-policy questions with regular OpenAI"""
        try:
            # Use direct OpenAI API for non-policy questions
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are an AI HR Assistant for 1957 Ventures company. You help employees with HR-related questions and can assist with form submissions.

Employee Information:
- Name: {employee['name']}
- Grade: {employee['grade']}
- Department: {employee['department']}
- Title: {employee['title']}

Current HR Status:
{context}

Instructions:
1. Answer HR questions accurately
2. Be helpful and professional
3. For specific requests like "request sick leave", guide them to submit a formal request
4. Always reference actual data when available
5. Keep responses concise but informative
6. For policy questions, suggest checking the Policy Center
7. If you don't know something, be honest and suggest contacting HR directly"""
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            response_type = self._determine_response_type(message)
            return {
                "response": response.choices[0].message.content,
                "type": response_type
            }
            
        except Exception as e:
            print(f"Regular AI Service Error: {str(e)}")
            return await self._fallback_response(message, employee['id'], context)
    
    
    async def _handle_policy_fallback(self, message: str, employee_id: str, context: str) -> Dict[str, Any]:
        """Fallback for policy questions when custom GPT fails"""
        try:
            # Try to find relevant policies from database
            policies = await policies_collection.find().to_list(100)
            
            # Simple keyword matching for policies
            message_lower = message.lower()
            relevant_policies = []
            
            for policy in policies:
                if any(keyword in message_lower for keyword in ['leave', 'vacation', 'sick']) and policy['category'] == 'Leaves':
                    relevant_policies.append(policy)
                elif any(keyword in message_lower for keyword in ['travel', 'business trip']) and policy['category'] == 'Travel':
                    relevant_policies.append(policy)
                elif any(keyword in message_lower for keyword in ['salary', 'compensation', 'pay']) and policy['category'] == 'Compensation':
                    relevant_policies.append(policy)
                elif any(keyword in message_lower for keyword in ['conduct', 'rules', 'dress', 'hours']) and policy['category'] == 'Conduct':
                    relevant_policies.append(policy)
            
            if relevant_policies:
                policy_info = []
                for policy in relevant_policies[:2]:  # Limit to 2 most relevant
                    policy_info.append(f"**{policy['title']}**: {policy['content'][:200]}...")
                
                response = f"Here's what I found in our policies:\n\n" + "\n\n".join(policy_info)
                response += "\n\nFor complete policy details, please check the Policy Center."
                
                return {
                    "response": response,
                    "type": "policy"
                }
            else:
                return {
                    "response": "I couldn't find specific policy information for your question. Please check the Policy Center or contact HR for detailed policy information.",
                    "type": "policy"
                }
                
        except Exception as e:
            print(f"Policy fallback error: {str(e)}")
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