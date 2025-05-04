// src/App.tsx
import React, { JSX } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home.tsx';
import Pref from './pages/Pref.tsx';
import Login from './pages/Login.tsx';
import SignUp from './pages/SignUp.tsx';
import DashBoard from './pages/DashBoard.tsx';
import { useUserStore } from './userState.ts';

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
    </Routes>
  );
}

export default App;
