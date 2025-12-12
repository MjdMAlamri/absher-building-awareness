import axios from 'axios';

// Backend URL - يمكن تغييره حسب البيئة
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds timeout
});

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      error.message = 'انتهت مهلة الاتصال. الخادم يستغرق وقتاً طويلاً.'
    } else if (error.response) {
      error.message = `خطأ من الخادم: ${error.response.status} - ${error.response.data?.detail || error.message}`
    } else if (error.request) {
      error.message = 'لا يمكن الاتصال بالخادم. تأكد من تشغيله على port 8000'
    }
    return Promise.reject(error)
  }
);

export const adminAPI = {
  // Get all visits with details
  async getVisits(filters = {}) {
    const params = new URLSearchParams();
    params.append('limit', '30'); // Limit to 30 visits for faster loading (5 sec target)
    if (filters.national_id_hash) params.append('national_id_hash', filters.national_id_hash);
    if (filters.branch_id) params.append('branch_id', filters.branch_id);
    if (filters.start_date) params.append('start_date', filters.start_date);
    if (filters.end_date) params.append('end_date', filters.end_date);
    if (filters.risk_level) params.append('risk_level', filters.risk_level);
    if (filters.auth_method) params.append('auth_method', filters.auth_method);
    
    const queryString = params.toString();
    const url = queryString ? `/admin/visits?${queryString}` : '/admin/visits?limit=100';
    const response = await api.get(url);
    return response.data;
  },

  // Get visit statistics
  async getStatistics() {
    const response = await api.get('/admin/statistics');
    return response.data;
  },

  // Get user visit history
  async getUserHistory(national_id_hash) {
    const response = await api.get(`/admin/users/${national_id_hash}/history`);
    return response.data;
  },

  // Evaluate risk for a visit
  async evaluateRisk(visitData) {
    const response = await api.post('/evaluate-risk', visitData);
    return response.data;
  },

  // Get ML analysis for a visit
  async getMLAnalysis(visitId) {
    const response = await api.get(`/admin/ml-analysis/${visitId}`);
    return response.data;
  },
};

export default api;

