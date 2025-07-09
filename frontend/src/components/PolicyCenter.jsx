import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Filter, 
  BookOpen, 
  Tag, 
  Calendar,
  FileText,
  Users,
  Briefcase,
  Heart,
  Plane,
  Loader2,
  AlertCircle
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { policiesApi } from '../services/api';

const PolicyCenter = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedPolicy, setSelectedPolicy] = useState(null);
  const [policies, setPolicies] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const categoryIcons = {
    'all': BookOpen,
    'Leaves': Calendar,
    'Compensation': Users,
    'Travel': Plane,
    'Conduct': Briefcase
  };

  const categoryLabels = {
    'all': 'All Categories',
    'Leaves': 'Leave Policies',
    'Compensation': 'Compensation',
    'Travel': 'Travel & Business',
    'Conduct': 'Work Rules'
  };

  useEffect(() => {
    fetchInitialData();
  }, []);

  useEffect(() => {
    fetchPolicies();
  }, [selectedCategory, searchTerm]);

  const fetchInitialData = async () => {
    try {
      setLoading(true);
      const [policiesData, categoriesData] = await Promise.all([
        policiesApi.getPolicies(),
        policiesApi.getCategories()
      ]);
      
      setPolicies(policiesData);
      setCategories(['all', ...categoriesData.categories]);
    } catch (err) {
      setError('Failed to load policies');
      console.error('Policy center error:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchPolicies = async () => {
    try {
      const category = selectedCategory === 'all' ? null : selectedCategory;
      const search = searchTerm.trim() || null;
      
      const data = await policiesApi.getPolicies(category, search);
      setPolicies(data);
    } catch (err) {
      console.error('Error fetching policies:', err);
      setError('Failed to load policies');
    }
  };

  const handlePolicySelect = async (policyId) => {
    try {
      const policy = await policiesApi.getPolicy(policyId);
      setSelectedPolicy(policy);
    } catch (err) {
      console.error('Error fetching policy:', err);
      setError('Failed to load policy details');
    }
  };

  const getCategoryIcon = (category) => {
    return categoryIcons[category] || FileText;
  };

  const getCategoryLabel = (category) => {
    return categoryLabels[category] || category;
  };

  const formatPolicyContent = (content) => {
    return content
      .split('\n')
      .map((line, index) => {
        if (line.startsWith('**') && line.endsWith('**')) {
          return <h4 key={index} className="font-bold text-lg mt-4 mb-2 text-gray-900">{line.slice(2, -2)}</h4>;
        }
        if (line.startsWith('-')) {
          return <li key={index} className="ml-4 mb-1 text-gray-700">{line.slice(1).trim()}</li>;
        }
        if (line.trim() === '') {
          return <br key={index} />;
        }
        return <p key={index} className="mb-2 text-gray-700">{line}</p>;
      });
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
          <p className="text-gray-600">Loading policies...</p>
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

  if (selectedPolicy) {
    const CategoryIcon = getCategoryIcon(selectedPolicy.category);
    
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6">
        <div className="max-w-4xl mx-auto space-y-6">
          <div className="flex items-center space-x-4">
            <Button 
              variant="outline" 
              onClick={() => setSelectedPolicy(null)}
              className="hover:bg-blue-50"
            >
              ← Back to Policies
            </Button>
          </div>

          <Card className="shadow-lg">
            <CardHeader className="bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-t-lg">
              <div className="flex items-center space-x-3">
                <CategoryIcon className="h-6 w-6" />
                <div className="flex-1">
                  <CardTitle className="text-2xl">{selectedPolicy.title}</CardTitle>
                  <div className="flex items-center space-x-4 mt-2">
                    <Badge variant="secondary" className="bg-white bg-opacity-20 text-white">
                      {selectedPolicy.category}
                    </Badge>
                    <span className="text-blue-100 text-sm">
                      Last updated: {formatDate(selectedPolicy.last_updated)}
                    </span>
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-8">
              <div className="prose max-w-none">
                {formatPolicyContent(selectedPolicy.content)}
              </div>
              
              <div className="mt-8 pt-6 border-t border-gray-200">
                <div className="flex flex-wrap gap-2">
                  <span className="text-sm font-medium text-gray-600 mr-2">Tags:</span>
                  {selectedPolicy.tags.map((tag) => (
                    <Badge key={tag} variant="outline" className="text-blue-600 border-blue-200">
                      <Tag className="h-3 w-3 mr-1" />
                      {tag}
                    </Badge>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-6">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Policy Center 📚
          </h1>
          <p className="text-lg text-gray-600">
            Search and browse company policies and procedures
          </p>
        </div>

        {/* Search and Filters */}
        <Card className="shadow-lg">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <Input
                  placeholder="Search policies, keywords, or content..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                <SelectTrigger className="w-full md:w-[200px]">
                  <Filter className="h-4 w-4 mr-2" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {categories.map((category) => {
                    const Icon = getCategoryIcon(category);
                    return (
                      <SelectItem key={category} value={category}>
                        <div className="flex items-center space-x-2">
                          <Icon className="h-4 w-4" />
                          <span>{getCategoryLabel(category)}</span>
                        </div>
                      </SelectItem>
                    );
                  })}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Category Quick Access */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {categories.slice(1).map((category) => {
            const Icon = getCategoryIcon(category);
            const count = policies.filter(p => p.category === category).length;
            return (
              <Card 
                key={category}
                className="cursor-pointer shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 group"
                onClick={() => setSelectedCategory(category)}
              >
                <CardContent className="p-4 text-center">
                  <Icon className="h-8 w-8 mx-auto mb-2 text-blue-600 group-hover:text-purple-600 transition-colors" />
                  <h3 className="font-medium text-sm text-gray-900">{getCategoryLabel(category)}</h3>
                  <p className="text-xs text-gray-500 mt-1">{count} policies</p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Search Results */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-gray-900">
              {searchTerm ? `Search Results (${policies.length})` : 'All Policies'}
            </h2>
            {selectedCategory !== 'all' && (
              <Button 
                variant="outline" 
                onClick={() => setSelectedCategory('all')}
                className="text-blue-600 border-blue-200 hover:bg-blue-50"
              >
                Clear Filter
              </Button>
            )}
          </div>

          {policies.length === 0 ? (
            <Card className="shadow-lg">
              <CardContent className="p-12 text-center">
                <BookOpen className="h-16 w-16 mx-auto mb-4 text-gray-300" />
                <h3 className="text-xl font-medium text-gray-900 mb-2">No policies found</h3>
                <p className="text-gray-600">Try adjusting your search terms or filters</p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {policies.map((policy) => {
                const CategoryIcon = getCategoryIcon(policy.category);
                return (
                  <Card 
                    key={policy.id}
                    className="cursor-pointer shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 group"
                    onClick={() => handlePolicySelect(policy.id)}
                  >
                    <CardHeader>
                      <div className="flex items-start space-x-3">
                        <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-2 rounded-lg group-hover:scale-110 transition-transform duration-300">
                          <CategoryIcon className="h-5 w-5 text-white" />
                        </div>
                        <div className="flex-1">
                          <CardTitle className="text-lg group-hover:text-blue-600 transition-colors">
                            {policy.title}
                          </CardTitle>
                          <div className="flex items-center space-x-2 mt-2">
                            <Badge variant="secondary" className="text-xs">
                              {policy.category}
                            </Badge>
                            <span className="text-xs text-gray-500">
                              Updated {formatDate(policy.last_updated)}
                            </span>
                          </div>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                        {policy.content.substring(0, 150)}...
                      </p>
                      <div className="flex flex-wrap gap-1">
                        {policy.tags.slice(0, 3).map((tag) => (
                          <Badge key={tag} variant="outline" className="text-xs">
                            {tag}
                          </Badge>
                        ))}
                        {policy.tags.length > 3 && (
                          <Badge variant="outline" className="text-xs">
                            +{policy.tags.length - 3} more
                          </Badge>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PolicyCenter;