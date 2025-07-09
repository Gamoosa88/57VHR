import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Current employee ID (in a real app, this would come from authentication)
const CURRENT_EMPLOYEE_ID = 'EMP001';
const CURRENT_SESSION_ID = 'session_' + Date.now();

// API client with error handling
const apiClient = axios.create({
  baseURL: API,
  timeout: 10000,
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`Making API request to: ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Employee API
export const employeeApi = {
  getCurrentEmployee: async () => {
    const response = await apiClient.get(`/employees/${CURRENT_EMPLOYEE_ID}`);
    return response.data;
  },
  
  getAllEmployees: async () => {
    const response = await apiClient.get('/employees');
    return response.data;
  }
};

// Dashboard API
export const dashboardApi = {
  getDashboardData: async () => {
    const response = await apiClient.get(`/dashboard/${CURRENT_EMPLOYEE_ID}`);
    return response.data;
  }
};

// HR Requests API
export const hrRequestsApi = {
  getRequests: async () => {
    const response = await apiClient.get(`/hr-requests/${CURRENT_EMPLOYEE_ID}`);
    return response.data;
  },
  
  createRequest: async (requestData) => {
    const response = await apiClient.post('/hr-requests', {
      ...requestData,
      employee_id: CURRENT_EMPLOYEE_ID
    });
    return response.data;
  },
  
  updateRequestStatus: async (requestId, status, approvedBy = null) => {
    const response = await apiClient.put(`/hr-requests/${requestId}/status`, {
      status,
      approved_by: approvedBy
    });
    return response.data;
  }
};

// Policies API
export const policiesApi = {
  getPolicies: async (category = null, search = null) => {
    const params = {};
    if (category) params.category = category;
    if (search) params.search = search;
    
    const response = await apiClient.get('/policies', { params });
    return response.data;
  },
  
  getPolicy: async (policyId) => {
    const response = await apiClient.get(`/policies/${policyId}`);
    return response.data;
  },
  
  getCategories: async () => {
    const response = await apiClient.get('/policies/categories');
    return response.data;
  }
};

// Chat API
export const chatApi = {
  sendMessage: async (message) => {
    const response = await apiClient.post('/chat/message', {
      employee_id: CURRENT_EMPLOYEE_ID,
      session_id: CURRENT_SESSION_ID,
      message
    });
    return response.data;
  },
  
  getChatHistory: async (sessionId = null) => {
    const params = {};
    if (sessionId) params.session_id = sessionId;
    
    const response = await apiClient.get(`/chat/history/${CURRENT_EMPLOYEE_ID}`, { params });
    return response.data;
  }
};

// Additional utility APIs
export const utilityApi = {
  getVacationBalance: async () => {
    const response = await apiClient.get(`/vacation-balance/${CURRENT_EMPLOYEE_ID}`);
    return response.data;
  },
  
  getSalaryPayments: async () => {
    const response = await apiClient.get(`/salary-payments/${CURRENT_EMPLOYEE_ID}`);
    return response.data;
  }
};

// Export current user info
export const getCurrentEmployeeId = () => CURRENT_EMPLOYEE_ID;
export const getCurrentSessionId = () => CURRENT_SESSION_ID;