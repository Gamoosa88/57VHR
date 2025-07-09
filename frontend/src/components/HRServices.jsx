import React, { useState } from 'react';
import { 
  Calendar, 
  Heart, 
  Home, 
  FileText, 
  CreditCard, 
  Plane,
  Plus,
  Send
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Calendar as CalendarComponent } from './ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from './ui/popover';
import { mockHRRequests, mockFormSubmissions } from '../data/mockData';
import { useToast } from '../hooks/use-toast';

const HRServices = () => {
  const [activeService, setActiveService] = useState(null);
  const [formData, setFormData] = useState({});
  const { toast } = useToast();

  const services = [
    {
      id: 'vacation',
      title: 'Vacation Leave',
      icon: Calendar,
      description: 'Request annual vacation leave',
      color: 'from-blue-500 to-blue-600'
    },
    {
      id: 'sick',
      title: 'Sick Leave', 
      icon: Heart,
      description: 'Request medical leave',
      color: 'from-red-500 to-red-600'
    },
    {
      id: 'wfh',
      title: 'Work from Home',
      icon: Home,
      description: 'Request remote work day',
      color: 'from-green-500 to-green-600'
    },
    {
      id: 'certificate',
      title: 'Salary Certificate',
      icon: FileText,
      description: 'Request salary verification',
      color: 'from-purple-500 to-purple-600'
    },
    {
      id: 'expense',
      title: 'Expense Reimbursement',
      icon: CreditCard,
      description: 'Submit expense claims',
      color: 'from-orange-500 to-orange-600'
    },
    {
      id: 'travel',
      title: 'Business Trip',
      icon: Plane,
      description: 'Request business travel',
      color: 'from-indigo-500 to-indigo-600'
    }
  ];

  const handleFormSubmit = (e) => {
    e.preventDefault();
    
    // Mock form submission
    setTimeout(() => {
      const response = Math.random() > 0.1 ? mockFormSubmissions.success : mockFormSubmissions.error;
      
      if (response.status === 'Submitted Successfully') {
        toast({
          title: "Request Submitted",
          description: response.message,
          variant: "default"
        });
        setActiveService(null);
        setFormData({});
      } else {
        toast({
          title: "Submission Failed",
          description: response.message,
          variant: "destructive"
        });
      }
    }, 1000);
  };

  const renderForm = () => {
    const service = services.find(s => s.id === activeService);
    if (!service) return null;

    return (
      <Card className="mt-6 shadow-lg">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <service.icon className="h-5 w-5" />
            <span>{service.title} Request</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleFormSubmit} className="space-y-6">
            {/* Common fields for all leave types */}
            {(activeService === 'vacation' || activeService === 'sick') && (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="startDate">Start Date</Label>
                    <Input
                      id="startDate"
                      type="date"
                      required
                      className="mt-1"
                      onChange={(e) => setFormData({...formData, startDate: e.target.value})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="endDate">End Date</Label>
                    <Input
                      id="endDate"
                      type="date"
                      required
                      className="mt-1"
                      onChange={(e) => setFormData({...formData, endDate: e.target.value})}
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="reason">Reason</Label>
                  <Textarea
                    id="reason"
                    placeholder="Please provide reason for leave..."
                    className="mt-1"
                    onChange={(e) => setFormData({...formData, reason: e.target.value})}
                  />
                </div>
              </>
            )}

            {/* Work from Home specific */}
            {activeService === 'wfh' && (
              <>
                <div>
                  <Label htmlFor="wfhDate">Work from Home Date</Label>
                  <Input
                    id="wfhDate"
                    type="date"
                    required
                    className="mt-1"
                    onChange={(e) => setFormData({...formData, date: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="wfhReason">Reason</Label>
                  <Textarea
                    id="wfhReason"
                    placeholder="Please provide reason for working from home..."
                    required
                    className="mt-1"
                    onChange={(e) => setFormData({...formData, reason: e.target.value})}
                  />
                </div>
              </>
            )}

            {/* Salary Certificate */}
            {activeService === 'certificate' && (
              <>
                <div>
                  <Label htmlFor="purpose">Purpose</Label>
                  <Select onValueChange={(value) => setFormData({...formData, purpose: value})}>
                    <SelectTrigger className="mt-1">
                      <SelectValue placeholder="Select purpose" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="bank">Bank Loan</SelectItem>
                      <SelectItem value="visa">Visa Application</SelectItem>
                      <SelectItem value="housing">Housing Application</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="details">Additional Details</Label>
                  <Textarea
                    id="details"
                    placeholder="Any additional information..."
                    className="mt-1"
                    onChange={(e) => setFormData({...formData, details: e.target.value})}
                  />
                </div>
              </>
            )}

            {/* Expense Reimbursement */}
            {activeService === 'expense' && (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="amount">Amount (SAR)</Label>
                    <Input
                      id="amount"
                      type="number"
                      step="0.01"
                      required
                      className="mt-1"
                      onChange={(e) => setFormData({...formData, amount: e.target.value})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="expenseDate">Expense Date</Label>
                    <Input
                      id="expenseDate"
                      type="date"
                      required
                      className="mt-1"
                      onChange={(e) => setFormData({...formData, expenseDate: e.target.value})}
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="category">Category</Label>
                  <Select onValueChange={(value) => setFormData({...formData, category: value})}>
                    <SelectTrigger className="mt-1">
                      <SelectValue placeholder="Select category" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="travel">Travel</SelectItem>
                      <SelectItem value="meals">Meals</SelectItem>
                      <SelectItem value="accommodation">Accommodation</SelectItem>
                      <SelectItem value="supplies">Office Supplies</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    placeholder="Describe the expense..."
                    required
                    className="mt-1"
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                  />
                </div>
              </>
            )}

            {/* Business Trip */}
            {activeService === 'travel' && (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="destination">Destination</Label>
                    <Input
                      id="destination"
                      required
                      placeholder="City, Country"
                      className="mt-1"
                      onChange={(e) => setFormData({...formData, destination: e.target.value})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="duration">Duration (days)</Label>
                    <Input
                      id="duration"
                      type="number"
                      required
                      className="mt-1"
                      onChange={(e) => setFormData({...formData, duration: e.target.value})}
                    />
                  </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="departureDate">Departure Date</Label>
                    <Input
                      id="departureDate"
                      type="date"
                      required
                      className="mt-1"
                      onChange={(e) => setFormData({...formData, departureDate: e.target.value})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="returnDate">Return Date</Label>
                    <Input
                      id="returnDate"
                      type="date"
                      required
                      className="mt-1"
                      onChange={(e) => setFormData({...formData, returnDate: e.target.value})}
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="businessPurpose">Business Purpose</Label>
                  <Textarea
                    id="businessPurpose"
                    placeholder="Describe the purpose of the trip..."
                    required
                    className="mt-1"
                    onChange={(e) => setFormData({...formData, businessPurpose: e.target.value})}
                  />
                </div>
              </>
            )}

            <div className="flex space-x-4 pt-4">
              <Button type="submit" className="flex-1">
                <Send className="h-4 w-4 mr-2" />
                Submit Request
              </Button>
              <Button 
                type="button" 
                variant="outline" 
                onClick={() => setActiveService(null)}
                className="flex-1"
              >
                Cancel
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            HR Services 📋
          </h1>
          <p className="text-lg text-gray-600">
            Submit requests and manage your HR needs
          </p>
        </div>

        {/* Service Grid */}
        {!activeService && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {services.map((service) => {
              const Icon = service.icon;
              return (
                <Card 
                  key={service.id}
                  className="cursor-pointer shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 group"
                  onClick={() => setActiveService(service.id)}
                >
                  <CardHeader>
                    <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${service.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                      <Icon className="h-6 w-6 text-white" />
                    </div>
                    <CardTitle className="text-xl">{service.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600 mb-4">{service.description}</p>
                    <Button className="w-full" variant="outline">
                      <Plus className="h-4 w-4 mr-2" />
                      Start Request
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}

        {/* Form */}
        {renderForm()}

        {/* Recent Requests */}
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle>Recent Requests</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {mockHRRequests.map((request) => (
                <div key={request.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900">{request.type}</h4>
                    <p className="text-sm text-gray-500">
                      {request.startDate && request.endDate 
                        ? `${new Date(request.startDate).toLocaleDateString()} - ${new Date(request.endDate).toLocaleDateString()}`
                        : request.date 
                        ? new Date(request.date).toLocaleDateString()
                        : `Submitted on ${new Date(request.submittedDate).toLocaleDateString()}`
                      }
                    </p>
                    {request.days && (
                      <p className="text-sm text-blue-600">{request.days} days</p>
                    )}
                  </div>
                  <Badge variant={request.status === 'Approved' ? 'default' : 'secondary'}>
                    {request.status}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default HRServices;