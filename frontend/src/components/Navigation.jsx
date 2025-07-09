import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  FileText, 
  BookOpen, 
  MessageCircle, 
  User,
  LogOut,
  Building2
} from 'lucide-react';
import { Button } from './ui/button';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { mockEmployee } from '../data/mockData';

const Navigation = () => {
  const location = useLocation();
  
  const navigationItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/services', icon: FileText, label: 'HR Services' },
    { path: '/policies', icon: BookOpen, label: 'Policy Center' },
    { path: '/chat', icon: MessageCircle, label: 'AI Assistant' }
  ];

  const isActive = (path) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <div className="bg-white border-r border-gray-200 h-screen w-64 fixed left-0 top-0 flex flex-col">
      {/* Logo and Company */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-lg">
            <Building2 className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-lg text-gray-900">1957 Ventures</h1>
            <p className="text-sm text-gray-500">HR Hub</p>
          </div>
        </div>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                isActive(item.path)
                  ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`}
            >
              <Icon className="h-5 w-5" />
              <span className="font-medium">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* User Profile Section */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex items-center space-x-3 mb-4">
          <Avatar className="h-10 w-10">
            <AvatarImage src="/api/placeholder/40/40" />
            <AvatarFallback className="bg-blue-100 text-blue-700">
              {mockEmployee.name.split(' ').map(n => n[0]).join('')}
            </AvatarFallback>
          </Avatar>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">
              {mockEmployee.name}
            </p>
            <p className="text-xs text-gray-500 truncate">
              {mockEmployee.title}
            </p>
          </div>
        </div>
        
        <div className="space-y-2">
          <Button variant="ghost" size="sm" className="w-full justify-start">
            <User className="h-4 w-4 mr-2" />
            Profile
          </Button>
          <Button variant="ghost" size="sm" className="w-full justify-start text-red-600 hover:text-red-700 hover:bg-red-50">
            <LogOut className="h-4 w-4 mr-2" />
            Logout
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Navigation;