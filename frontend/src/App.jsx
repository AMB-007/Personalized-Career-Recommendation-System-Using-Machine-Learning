import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import StudentProfile from './pages/StudentProfile';
import DynamicTest from './pages/DynamicTest';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import History from './pages/History';
import Admin from './pages/Admin';
import AdminLogin from './pages/AdminLogin';
import UserSettings from './pages/UserSettings';
import Home from './pages/Home';

function App() {
  return (
    <ThemeProvider>
      <Router>
        <div className="app-container">
          <header>
            <Navbar />
          </header>
          
          <main className="main-content">
            <Routes>
              {/* Public User Routes */}
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/admin-login" element={<AdminLogin />} />

              {/* Protected Assessment & User Routes */}
              <Route path="/assessment" element={<ProtectedRoute><StudentProfile /></ProtectedRoute>} />
              <Route path="/test" element={<ProtectedRoute><DynamicTest /></ProtectedRoute>} />
              <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
              <Route path="/history" element={<ProtectedRoute><History /></ProtectedRoute>} />
              <Route path="/settings" element={<ProtectedRoute><UserSettings /></ProtectedRoute>} />

              {/* Admin Portal Routes */}
              <Route path="/admin" element={<Admin />} />
            </Routes>
          </main>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
