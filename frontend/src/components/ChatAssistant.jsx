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
  BookOpen,
  Loader2,
  AlertCircle
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { ScrollArea } from './ui/scroll-area';
import { chatApi, employeeApi } from '../services/api';

const ChatAssistant = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [employee, setEmployee] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    try {
      setLoading(true);
      const [chatHistory, empData] = await Promise.all([
        chatApi.getChatHistory(),
        employeeApi.getCurrentEmployee()
      ]);
      
      setMessages(chatHistory.messages || []);
      setEmployee(empData);
    } catch (err) {
      setError('Failed to load chat history');
      console.error('Chat assistant error:', err);
    } finally {
      setLoading(false);
    }
  };

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

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isTyping) return;

    const userMessage = {
      id: `msg_${Date.now()}`,
      message: inputMessage,
      timestamp: new Date().toISOString(),
      type: 'user'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    try {
      const response = await chatApi.sendMessage(inputMessage);
      
      const assistantMessage = {
        id: response.id,
        message: inputMessage,
        response: response.response,
        timestamp: response.timestamp,
        type: response.type
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Chat error:', err);
      const errorMessage = {
        id: `error_${Date.now()}`,
        message: inputMessage,
        response: "I'm sorry, I encountered an error processing your request. Please try again.",
        timestamp: new Date().toISOString(),
        type: 'error'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
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

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading chat assistant...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-8 w-8 text-red-600 mx-auto mb-4" />
          <p className="text-red-600">{error}</p>
          <Button onClick={fetchInitialData} className="mt-4">
            Try Again
          </Button>
        </div>
      </div>
    );
  }

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
          {employee && (
            <p className="text-sm text-gray-500">
              Hi {employee.name}, I'm here to help with all your HR needs!
            </p>
          )}
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
                {messages.length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    <Bot className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                    <p>Start a conversation! Ask me anything about HR policies, requests, or your current status.</p>
                  </div>
                )}
                
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
                            <div className={`rounded-2xl rounded-bl-md px-4 py-2 ${
                              msg.type === 'error' ? 'bg-red-100' : 'bg-gray-100'
                            }`}>
                              <p className={`text-sm ${
                                msg.type === 'error' ? 'text-red-800' : 'text-gray-800'
                              }`}>
                                {msg.response}
                              </p>
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
                disabled={isTyping}
              />
              <Button 
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isTyping}
                className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700"
              >
                {isTyping ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Send className="h-4 w-4" />
                )}
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