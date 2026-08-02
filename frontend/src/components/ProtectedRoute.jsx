import { Navigate, useLocation } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const location = useLocation();
  const token = localStorage.getItem('token');
  const user = localStorage.getItem('user');

  const isAuthenticated = Boolean(token || user);

  if (!isAuthenticated) {
    return (
      <Navigate 
        to="/login" 
        state={{ 
          from: location.pathname, 
          message: 'Please sign in or create a free account to take the career assessment.' 
        }} 
        replace 
      />
    );
  }

  return children;
};

export default ProtectedRoute;
