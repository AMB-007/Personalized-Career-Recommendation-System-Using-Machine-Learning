// Environment variable configuration
// Reads from process.env (webpack) or import.meta.env (Vite-style)

const BASE_URL =
  process.env.REACT_APP_API_BASE_URL ||
  import.meta?.env?.VITE_API_BASE_URL ||
  '/api';

const TIMEOUT = parseInt(process.env.REACT_APP_API_TIMEOUT || '10000', 10);

const isAnalyticsEnabled =
  process.env.REACT_APP_ENABLE_ANALYTICS === 'true' ||
  import.meta?.env?.VITE_ENABLE_ANALYTICS === 'true';

const isMockDataEnabled =
  process.env.REACT_APP_ENABLE_MOCK_DATA === 'true' ||
  import.meta?.env?.VITE_ENABLE_MOCK_DATA === 'true';

export const API_CONFIG = {
  BASE_URL,
  TIMEOUT,
  isAnalyticsEnabled,
  isMockDataEnabled,
  getFullUrl: (endpoint) => `${BASE_URL}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`
};

// Create an Axios instance with defaults
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Request interceptor for adding auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;