import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Calendar, 
  Clock, 
  DollarSign, 
  Plane, 
  FileText,
  TrendingUp,
  AlertCircle,
  CheckCircle2,
  Loader2
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { dashboardApi, employeeApi } from '../services/api';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [dashData, empData] = await Promise.all([
        dashboardApi.getDashboardData(),
        employeeApi.getCurrentEmployee()
      ]);
      setDashboardData(dashData);
      setEmployee(empData);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'approved': return 'bg-green-100 text-green-800';
      case 'pending approval': return 'bg-yellow-100 text-yellow-800';
      case 'under review': return 'bg-blue-100 text-blue-800';
      case 'paid': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-SA', {
      style: 'currency',
      currency: 'SAR'
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading dashboard...</p>
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
          <Button onClick={fetchDashboardData} className="mt-4">
            Try Again
          </Button>
        </div>
      </div>
    );
  }

  if (!dashboardData || !employee) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Welcome Header */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Welcome back, {employee.name.split(' ')[0]}! 👋
          </h1>
          <p className="text-lg text-gray-600">
            Here's what's happening with your HR activities
          </p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Vacation Days */}
          <Card className="bg-gradient-to-br from-green-500 to-green-600 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center space-x-2 text-white">
                <Calendar className="h-5 w-5" />
                <span>Vacation Days</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold mb-1">{dashboardData.vacationDaysLeft}</div>
              <p className="text-green-100">Days remaining</p>
              <div className="mt-2 bg-green-400 bg-opacity-30 rounded-full h-2">
                <div 
                  className="bg-white h-2 rounded-full transition-all duration-500"
                  style={{ width: `${(dashboardData.vacationDaysLeft / 30) * 100}%` }}
                ></div>
              </div>
            </CardContent>
          </Card>

          {/* Pending Requests */}
          <Card className="bg-gradient-to-br from-orange-500 to-red-500 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center space-x-2 text-white">
                <Clock className="h-5 w-5" />
                <span>Pending Requests</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold mb-1">{dashboardData.pendingRequests.length}</div>
              <p className="text-orange-100">Awaiting approval</p>
              {dashboardData.pendingRequests.length > 0 && (
                <div className="mt-2 flex items-center space-x-1">
                  <AlertCircle className="h-4 w-4" />
                  <span className="text-sm">{dashboardData.pendingRequests[0].type}</span>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Last Salary */}
          <Card className="bg-gradient-to-br from-blue-500 to-blue-600 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center space-x-2 text-white">
                <DollarSign className="h-5 w-5" />
                <span>Last Salary</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold mb-1">{formatCurrency(dashboardData.lastSalaryPayment.amount)}</div>
              <p className="text-blue-100">{formatDate(dashboardData.lastSalaryPayment.date)}</p>
              <Badge className="mt-2 bg-blue-400 bg-opacity-30 text-white border-blue-300">
                <CheckCircle2 className="h-3 w-3 mr-1" />
                {dashboardData.lastSalaryPayment.status}
              </Badge>
            </CardContent>
          </Card>

          {/* Business Trip */}
          <Card className="bg-gradient-to-br from-purple-500 to-purple-600 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center space-x-2 text-white">
                <Plane className="h-5 w-5" />
                <span>Business Trip</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold mb-1">{dashboardData.businessTripStatus.current}</div>
              <p className="text-purple-100 text-sm">
                {dashboardData.businessTripStatus.startDate && formatDate(dashboardData.businessTripStatus.startDate)}
              </p>
              <Badge className="mt-2 bg-purple-400 bg-opacity-30 text-white border-purple-300">
                {dashboardData.businessTripStatus.status}
              </Badge>
            </CardContent>
          </Card>
        </div>

        {/* Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Recent Requests */}
          <Card className="lg:col-span-2 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <FileText className="h-5 w-5 text-blue-600" />
                <span>Recent Requests</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {dashboardData.pendingRequests.map((request) => (
                  <div key={request.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900">{request.type}</h4>
                      <p className="text-sm text-gray-500">
                        Submitted on {formatDate(request.submittedDate)}
                      </p>
                      {request.destination && (
                        <p className="text-sm text-blue-600">Destination: {request.destination}</p>
                      )}
                      {request.amount && (
                        <p className="text-sm text-green-600">Amount: {formatCurrency(request.amount)}</p>
                      )}
                    </div>
                    <Badge className={getStatusColor(request.status)}>
                      {request.status}
                    </Badge>
                  </div>
                ))}
                {dashboardData.pendingRequests.length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                    <p>No pending requests</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Upcoming Events */}
          <Card className="shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="h-5 w-5 text-purple-600" />
                <span>Upcoming</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {dashboardData.upcomingEvents.map((event, index) => (
                  <div key={index} className="flex items-center space-x-3 p-3 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg">
                    <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">{event.type}</p>
                      <p className="text-sm text-gray-500">{formatDate(event.date)}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Button className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white shadow-lg hover:shadow-xl transition-all duration-300">
                Request Leave
              </Button>
              <Button variant="outline" className="border-purple-200 text-purple-700 hover:bg-purple-50">
                Submit Expense
              </Button>
              <Button variant="outline" className="border-green-200 text-green-700 hover:bg-green-50">
                View Policies
              </Button>
              <Button variant="outline" className="border-orange-200 text-orange-700 hover:bg-orange-50">
                Ask AI Assistant
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;