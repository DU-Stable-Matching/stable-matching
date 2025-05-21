// src/App.tsx
import React, { JSX } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import Pref from './pages/Pref';
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import DashBoard from './pages/DashBoard';
import AdminPref from './pages/AdminPref';
import AdminDashBoard from './pages/AdminDashBoard';
import { useUserStore } from './userState';

const ProtectedRoute: React.FC<{ children: JSX.Element }> = ({ children }) => {
  const userID = useUserStore(state => state.userID);
  if (userID === null) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/" element={<Home />} />
      <Route path="/dashboard" element={<ProtectedRoute><DashBoard /></ProtectedRoute>} />
      <Route path="/user_pref" element={<ProtectedRoute><Pref /></ProtectedRoute>} />
      <Route path="/admin_pref" element={<ProtectedRoute><AdminPref /></ProtectedRoute>} />
      <Route path="/admin_dashboard" element={<ProtectedRoute><AdminDashBoard /></ProtectedRoute>} />
    </Routes>
  );
}

export default App;
