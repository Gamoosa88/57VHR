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
        
        # Note: Custom ChatGPT IDs (starting with 'g-') cannot be accessed via API
        # This service simulates custom GPT behavior using comprehensive policy context
        self.custom_gpt_id = "g-685d53e450208191992ef69c0eb2d63c-1957v-hr-assistant"  # Reference only
    
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
        """Check if the message is asking about policies (English and Arabic)"""
        policy_keywords = [
            # English keywords
            'policy', 'policies', 'rule', 'rules', 'procedure', 'procedures',
            'leave policy', 'vacation policy', 'sick leave policy', 'travel policy',
            'compensation policy', 'salary policy', 'work rules', 'conduct',
            'what is the policy', 'policy on', 'company policy', 'hr policy',
            'annual leave', 'sick leave', 'maternity leave', 'business travel',
            'end of service', 'performance management', 'recruitment',
            
            # Arabic keywords
            'سياسة', 'سياسات', 'قواعد', 'قانون', 'إجراءات', 'لوائح',
            'إجازة', 'إجازات', 'إجازة سنوية', 'إجازة مرضية', 'إجازة أمومة',
            'انتداب', 'سفر', 'راتب', 'رواتب', 'مزايا', 'تعويضات',
            'نهاية الخدمة', 'مكافأة', 'توظيف', 'تطوير', 'أداء',
            'ما هي السياسة', 'سياسة الشركة', 'قواعد العمل'
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in policy_keywords)
    
    async def _query_custom_gpt(self, message: str, employee: Dict, context: str) -> str:
        """Query a custom GPT-like system for policy-related questions with bilingual support"""
        
        # Get all policies from database to provide comprehensive context
        policies = await policies_collection.find().to_list(100)
        
        # Detect if query is in Arabic
        arabic_chars = ['ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي']
        is_arabic_query = any(char in message for char in arabic_chars)
        
        # Create comprehensive policy knowledge base
        policy_knowledge = ""
        for policy in policies:
            policy_knowledge += f"\n=== {policy['title']} ({policy['category']}) ===\n"
            
            # Include both English and Arabic content if available
            policy_knowledge += f"ENGLISH CONTENT:\n{policy['content']}\n"
            if 'content_ar' in policy and policy['content_ar']:
                policy_knowledge += f"\nARABIC CONTENT:\n{policy['content_ar']}\n"
            
            policy_knowledge += f"Tags: {', '.join(policy['tags'])}\n"
            policy_knowledge += f"Last Updated: {policy['last_updated']}\n\n"
        
        # Enhanced message with employee context
        enhanced_message = f"""
EMPLOYEE PROFILE:
- Name: {employee['name']}
- Employee ID: {employee.get('id', 'N/A')}
- Grade: {employee['grade']}
- Department: {employee['department']}
- Title: {employee['title']}
- Email: {employee.get('email', 'N/A')}
- Manager: {employee.get('manager', 'N/A')}

CURRENT HR STATUS:
{context}

EMPLOYEE QUESTION: {message}
"""
        
        try:
            # Determine response language based on query
            language_instruction = "Respond primarily in Arabic" if is_arabic_query else "Respond primarily in English"
            
            # Use OpenAI with comprehensive system prompt to simulate custom GPT behavior
            response = openai.chat.completions.create(
                model="gpt-4o",  # Using the latest model
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are the 1957 Ventures HR Assistant (مساعد الموارد البشرية لشركة الابتكار الجريء), a specialized bilingual AI assistant trained specifically on 1957 Ventures' HR policies and procedures. You have comprehensive knowledge of the company's HR policies in both English and Arabic.

COMPANY: 1957 Ventures Company (شركة الابتكار الجريء لحاضنات ومسرعات الأعمال)
ROLE: Official HR Assistant AI (مساعد الموارد البشرية الرسمي)

=== COMPLETE HR POLICY KNOWLEDGE BASE ===
{policy_knowledge}

=== YOUR EXPERTISE AREAS / مجالات خبرتك ===
- Leave policies (vacation, sick leave, emergency leave) / سياسات الإجازات
- Compensation and benefits / التعويضات والمزايا  
- Business travel policies and procedures / سياسات السفر والانتداب
- Work rules and conduct guidelines / قواعد العمل والسلوك
- Employee entitlements based on grade levels / استحقاقات الموظفين حسب الدرجات
- HR process guidance and form assistance / إرشادات العمليات والنماذج

=== RESPONSE GUIDELINES / إرشادات الإجابة ===
1. Always provide accurate, policy-based answers using the knowledge base above
2. Reference specific policy sections when applicable
3. Consider the employee's grade level for entitlements:
   - Grade D and above: 30 vacation days per year / الدرجة D فأعلى: 30 يوم إجازة سنوياً
   - Grade C and below: 25 vacation days per year / الدرجة C فأقل: 25 يوم إجازة سنوياً
4. Be professional, helpful, and comprehensive
5. {language_instruction} but include key terms in both languages when helpful
6. For policy clarifications, quote relevant sections
7. Always suggest checking the Policy Center for complete details
8. If information is not in the policies, clearly state so and suggest contacting HR directly

=== IMPORTANT NOTES / ملاحظات مهمة ===
- All policy information above is the complete and authoritative source
- Always maintain professional HR assistant tone
- Provide specific, actionable guidance when possible
- Include Arabic translation for key terms when responding in English
- Include English translation for key terms when responding in Arabic"""
                    },
                    {
                        "role": "user",
                        "content": enhanced_message
                    }
                ],
                max_tokens=1200,
                temperature=0.2,  # Lower temperature for more consistent, policy-focused responses
                top_p=0.9
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Custom GPT simulation error: {str(e)}")
            raise e
    
    async def _enhanced_policy_response(self, message: str, employee: Dict, context: str) -> str:
        """Enhanced policy response using database policies with AI formatting"""
        try:
            # Get all policies from database
            policies = await policies_collection.find().to_list(100)
            
            # Create a comprehensive policy context
            policy_context = ""
            for policy in policies:
                policy_context += f"\n**{policy['title']}** ({policy['category']}):\n{policy['content']}\n\n"
            
            # Use OpenAI to format response based on policies
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are the 1957 Ventures HR Assistant with access to comprehensive company policies. 
                        
You must answer policy questions using ONLY the information from the company policies provided below. Do not make up information or policies.

Company HR Policies:
{policy_context}

Employee Context:
- Name: {employee['name']}
- Grade: {employee['grade']} 
- Department: {employee['department']}
- Title: {employee['title']}

Current HR Status:
{context}

Instructions:
1. Answer policy questions accurately using only the provided policy information
2. Reference specific policy sections when relevant
3. Be helpful and professional
4. If asking about specific entitlements, check the employee's grade
5. Keep responses concise but comprehensive
6. If you cannot find the specific policy information, say so clearly"""
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Enhanced policy response error: {str(e)}")
            # Final fallback to basic policy search
            return await self._basic_policy_search(message)
    
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
    
    
    
    async def _basic_policy_search(self, message: str) -> str:
        """Basic policy search fallback"""
        try:
            policies = await policies_collection.find().to_list(100)
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
                response = "Here's what I found in our company policies:\n\n"
                for policy in relevant_policies[:2]:
                    response += f"**{policy['title']}**:\n{policy['content'][:300]}...\n\n"
                response += "For complete policy details, please check the Policy Center."
                return response
            else:
                return "I couldn't find specific policy information for your question. Please check the Policy Center or contact HR for detailed policy information."
                
        except Exception as e:
            print(f"Basic policy search error: {str(e)}")
            return "I'm having trouble accessing policy information right now. Please check the Policy Center or contact HR directly."
    
    async def _handle_policy_fallback(self, message: str, employee_id: str, context: str) -> Dict[str, Any]:
        """Fallback for policy questions when custom GPT fails"""
        try:
            response_text = await self._basic_policy_search(message)
            return {
                "response": response_text,
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