import React, { useState, useEffect } from 'react';
import { 
  Calendar, 
  Heart, 
  Home, 
  FileText, 
  CreditCard, 
  Plane,
  Plus,
  Send,
  Loader2
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { hrRequestsApi } from '../services/api';
import { useToast } from '../hooks/use-toast';

const HRServices = () => {
  const [activeService, setActiveService] = useState(null);
  const [formData, setFormData] = useState({});
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const { toast } = useToast();

  const services = [
    {
      id: 'Vacation Leave',
      title: 'Vacation Leave',
      icon: Calendar,
      description: 'Request annual vacation leave',
      color: 'from-blue-500 to-blue-600'
    },
    {
      id: 'Sick Leave', 
      title: 'Sick Leave',
      icon: Heart,
      description: 'Request medical leave',
      color: 'from-red-500 to-red-600'
    },
    {
      id: 'Work from Home',
      title: 'Work from Home',
      icon: Home,
      description: 'Request remote work day',
      color: 'from-green-500 to-green-600'
    },
    {
      id: 'Salary Certificate',
      title: 'Salary Certificate',
      icon: FileText,
      description: 'Request salary verification',
      color: 'from-purple-500 to-purple-600'
    },
    {
      id: 'Expense Reimbursement',
      title: 'Expense Reimbursement',
      icon: CreditCard,
      description: 'Submit expense claims',
      color: 'from-orange-500 to-orange-600'
    },
    {
      id: 'Business Trip',
      title: 'Business Trip',
      icon: Plane,
      description: 'Request business travel',
      color: 'from-indigo-500 to-indigo-600'
    }
  ];

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      setLoading(true);
      const data = await hrRequestsApi.getRequests();
      setRequests(data);
    } catch (error) {
      console.error('Error fetching requests:', error);
      toast({
        title: "Error",
        description: "Failed to load requests",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setSubmitting(true);
      
      // Prepare request data
      const requestData = {
        type: activeService,
        ...formData
      };
      
      await hrRequestsApi.createRequest(requestData);
      
      toast({
        title: "Request Submitted",
        description: "Your request has been submitted successfully and is pending approval.",
        variant: "default"
      });
      
      setActiveService(null);
      setFormData({});
      fetchRequests(); // Refresh the requests list
      
    } catch (error) {
      console.error('Error submitting request:', error);
      toast({
        title: "Submission Failed",
        description: "There was an error submitting your request. Please try again.",
        variant: "destructive"
      });
    } finally {
      setSubmitting(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
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
            {(activeService === 'Vacation Leave' || activeService === 'Sick Leave') && (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="startDate">Start Date</Label>
                    <Input
                      id="startDate"
                      type="date"
                      required
                      className="mt-1"
                      onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="endDate">End Date</Label>
                    <Input
                      id="endDate"
                      type="date"
                      required
                      className="mt-1"
                      onChange={(e) => setFormData({...formData, end_date: e.target.value})}
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
            {activeService === 'Work from Home' && (
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
            {activeService === 'Salary Certificate' && (
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
            {activeService === 'Expense Reimbursement' && (
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
                      onChange={(e) => setFormData({...formData, amount: parseFloat(e.target.value)})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="expenseDate">Expense Date</Label>
                    <Input
                      id="expenseDate"
                      type="date"
                      required
                      className="mt-1"
                      onChange={(e) => setFormData({...formData, date: e.target.value})}
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
            {activeService === 'Business Trip' && (
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
                      onChange={(e) => setFormData({...formData, duration: parseInt(e.target.value)})}
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
                      onChange={(e) => setFormData({...formData, departure_date: e.target.value})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="returnDate">Return Date</Label>
                    <Input
                      id="returnDate"
                      type="date"
                      required
                      className="mt-1"
                      onChange={(e) => setFormData({...formData, return_date: e.target.value})}
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
                    onChange={(e) => setFormData({...formData, business_purpose: e.target.value})}
                  />
                </div>
              </>
            )}

            <div className="flex space-x-4 pt-4">
              <Button type="submit" className="flex-1" disabled={submitting}>
                {submitting ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Submitting...
                  </>
                ) : (
                  <>
                    <Send className="h-4 w-4 mr-2" />
                    Submit Request
                  </>
                )}
              </Button>
              <Button 
                type="button" 
                variant="outline" 
                onClick={() => setActiveService(null)}
                className="flex-1"
                disabled={submitting}
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
            {loading ? (
              <div className="text-center py-8">
                <Loader2 className="h-6 w-6 animate-spin text-blue-600 mx-auto mb-4" />
                <p className="text-gray-600">Loading requests...</p>
              </div>
            ) : (
              <div className="space-y-4">
                {requests.slice(0, 5).map((request) => (
                  <div key={request.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900">{request.type}</h4>
                      <p className="text-sm text-gray-500">
                        {request.start_date && request.end_date 
                          ? `${formatDate(request.start_date)} - ${formatDate(request.end_date)}`
                          : request.date 
                          ? formatDate(request.date)
                          : `Submitted on ${formatDate(request.submitted_date)}`
                        }
                      </p>
                      {request.days && (
                        <p className="text-sm text-blue-600">{request.days} days</p>
                      )}
                      {request.amount && (
                        <p className="text-sm text-green-600">Amount: {request.amount} SAR</p>
                      )}
                      {request.destination && (
                        <p className="text-sm text-purple-600">Destination: {request.destination}</p>
                      )}
                    </div>
                    <Badge variant={request.status === 'Approved' ? 'default' : 'secondary'}>
                      {request.status}
                    </Badge>
                  </div>
                ))}
                {requests.length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                    <p>No requests submitted yet</p>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default HRServices;