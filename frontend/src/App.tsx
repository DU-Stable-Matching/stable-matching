// src/App.tsx
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home.tsx';
import Pref from './pages/Pref.tsx';
import Login from './pages/Login.tsx';
import { useUserStore } from './userState.ts';

const ProtectedRoute: React.FC<{ children: JSX.Element }> = ({ children }) => {
  const userID = useUserStore(state => state.userID);
  return userID ? children : <Navigate to="/login" replace />;
};

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
      <Route path="/user_pref" element={<ProtectedRoute><Pref /></ProtectedRoute>} />
    </Routes>
  );
}

export default App;
