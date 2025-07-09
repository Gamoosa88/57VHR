import React, { useState, useRef, useEffect } from 'react';
import { 
  Send, 
  Bot, 
  User, 
  MessageCircle, 
  Sparkles,
  Calendar,
  FileText,
  Clock,
  BookOpen
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { ScrollArea } from './ui/scroll-area';
import { mockChatHistory, mockEmployee, mockDashboardData } from '../data/mockData';

const ChatAssistant = () => {
  const [messages, setMessages] = useState(mockChatHistory);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const quickActions = [
    {
      icon: Calendar,
      text: "How many vacation days do I have?",
      category: "Leave"
    },
    {
      icon: FileText, 
      text: "Request a sick leave",
      category: "Request"
    },
    {
      icon: Clock,
      text: "What's my last salary payment?",
      category: "Salary"
    },
    {
      icon: BookOpen,
      text: "Show me the business travel policy",
      category: "Policy"
    }
  ];

  // Mock AI responses based on common HR queries
  const generateResponse = (message) => {
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('vacation') && lowerMessage.includes('days')) {
      return {
        response: `You currently have ${mockDashboardData.vacationDaysLeft} vacation days remaining out of your annual 30-day entitlement (Grade ${mockEmployee.grade}). You've used 2 days so far this year. Remember, you need to take at least 10 consecutive days once per year according to company policy.`,
        type: 'query'
      };
    }
    
    if (lowerMessage.includes('sick leave') && lowerMessage.includes('request')) {
      return {
        response: `I can help you request sick leave. According to our policy, you'll need to provide a medical certificate from an approved medical body. For the first 30 days, you'll receive full salary. Would you like me to guide you through the sick leave request form?`,
        type: 'action'
      };
    }
    
    if (lowerMessage.includes('salary') && (lowerMessage.includes('last') || lowerMessage.includes('payment'))) {
      return {
        response: `Your last salary payment was ${new Intl.NumberFormat('en-SA', { style: 'currency', currency: 'SAR' }).format(mockDashboardData.lastSalaryPayment.amount)} on ${new Date(mockDashboardData.lastSalaryPayment.date).toLocaleDateString()}. The payment status is "${mockDashboardData.lastSalaryPayment.status}". Salaries are paid monthly on the 15th of each month.`,
        type: 'query'
      };
    }
    
    if (lowerMessage.includes('business travel') || lowerMessage.includes('travel policy')) {
      return {
        response: `Based on your Grade ${mockEmployee.grade}, for business travel you're entitled to: Economy class tickets, 4-star hotel accommodation, and 200-400 SAR daily allowance inside the Kingdom (300-600 SAR outside). The company provides up to 14 days hotel stay and airport transfers. Would you like to see the full travel policy or request a business trip?`,
        type: 'policy'
      };
    }
    
    if (lowerMessage.includes('work from home') || lowerMessage.includes('wfh') || lowerMessage.includes('remote')) {
      return {
        response: `You can request work from home for a maximum of 2 days per month. The request cannot be at the beginning or end of the week and requires manager approval. Would you like me to help you submit a WFH request?`,
        type: 'policy'
      };
    }
    
    if (lowerMessage.includes('expense') && lowerMessage.includes('policy')) {
      return {
        response: `For expense reimbursement, you can claim business-related expenses with proper receipts. Categories include travel, meals, accommodation, office supplies, and other work-related expenses. All expenses must be approved by your manager and supported by original invoices. Would you like to submit an expense claim?`,
        type: 'policy'
      };
    }
    
    // Default response
    return {
      response: `I understand you're asking about "${message}". I'm here to help with HR-related questions about policies, leave requests, salary information, and more. Could you please be more specific about what you'd like to know? I can help with vacation days, sick leave requests, expense claims, business travel, work from home policies, and general HR inquiries.`,
      type: 'query'
    };
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: `chat${Date.now()}`,
      message: inputMessage,
      timestamp: new Date().toISOString(),
      type: 'user'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Simulate AI processing delay
    setTimeout(() => {
      const aiResponse = generateResponse(inputMessage);
      const assistantMessage = {
        id: `chat${Date.now() + 1}`,
        message: inputMessage,
        response: aiResponse.response,
        timestamp: new Date().toISOString(),
        type: aiResponse.type
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const handleQuickAction = (actionText) => {
    setInputMessage(actionText);
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            AI HR Assistant 🤖
          </h1>
          <p className="text-lg text-gray-600">
            Get instant answers to your HR questions and submit requests
          </p>
        </div>

        {/* Quick Actions */}
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Sparkles className="h-5 w-5 text-purple-600" />
              <span>Quick Actions</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {quickActions.map((action, index) => {
                const Icon = action.icon;
                return (
                  <Button
                    key={index}
                    variant="outline"
                    className="justify-start h-auto p-4 hover:bg-blue-50 hover:border-blue-200 transition-all duration-200"
                    onClick={() => handleQuickAction(action.text)}
                  >
                    <Icon className="h-4 w-4 mr-3 text-blue-600" />
                    <div className="text-left">
                      <div className="font-medium">{action.text}</div>
                      <Badge variant="secondary" className="mt-1 text-xs">
                        {action.category}
                      </Badge>
                    </div>
                  </Button>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Chat Interface */}
        <Card className="shadow-lg h-[600px] flex flex-col">
          <CardHeader className="bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-t-lg">
            <CardTitle className="flex items-center space-x-2">
              <MessageCircle className="h-5 w-5" />
              <span>Chat with HR Assistant</span>
            </CardTitle>
          </CardHeader>
          
          {/* Messages Area */}
          <div className="flex-1 overflow-hidden">
            <ScrollArea className="h-full p-4">
              <div className="space-y-4">
                {messages.map((msg) => (
                  <div key={msg.id} className="space-y-3">
                    {/* User Message */}
                    {msg.type === 'user' ? (
                      <div className="flex justify-end">
                        <div className="flex items-end space-x-2 max-w-[80%]">
                          <div className="bg-blue-600 text-white rounded-2xl rounded-br-md px-4 py-2">
                            <p className="text-sm">{msg.message}</p>
                          </div>
                          <div className="bg-blue-100 p-2 rounded-full">
                            <User className="h-4 w-4 text-blue-600" />
                          </div>
                        </div>
                      </div>
                    ) : (
                      <>
                        {/* Assistant Message */}
                        <div className="flex justify-start">
                          <div className="flex items-end space-x-2 max-w-[80%]">
                            <div className="bg-gradient-to-r from-purple-500 to-blue-500 p-2 rounded-full">
                              <Bot className="h-4 w-4 text-white" />
                            </div>
                            <div className="bg-gray-100 rounded-2xl rounded-bl-md px-4 py-2">
                              <p className="text-sm text-gray-800">{msg.response}</p>
                              <span className="text-xs text-gray-500 mt-1 block">
                                {formatTimestamp(msg.timestamp)}
                              </span>
                            </div>
                          </div>
                        </div>
                      </>
                    )}
                  </div>
                ))}
                
                {/* Typing Indicator */}
                {isTyping && (
                  <div className="flex justify-start">
                    <div className="flex items-end space-x-2">
                      <div className="bg-gradient-to-r from-purple-500 to-blue-500 p-2 rounded-full">
                        <Bot className="h-4 w-4 text-white" />
                      </div>
                      <div className="bg-gray-100 rounded-2xl rounded-bl-md px-4 py-2">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>
            </ScrollArea>
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-200 p-4">
            <div className="flex space-x-2">
              <Input
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Ask me anything about HR policies, leave requests, or submit a request..."
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                className="flex-1"
              />
              <Button 
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isTyping}
                className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
            <p className="text-xs text-gray-500 mt-2">
              💡 Try asking: "How many vacation days do I have?" or "Request a sick leave"
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default ChatAssistant;