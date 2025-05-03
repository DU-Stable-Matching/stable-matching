import React from 'react';
import Home from './pages/Home.tsx';
import { Routes, Route } from "react-router-dom";
import Login from './pages/Login.tsx';


function App() {
  return (
    <div>
        <Routes>
          <Route path="/" element={<Home/>}/>
          <Route path="/login" element={<Login/>}/>
        </Routes>
    </div>
  );
}

export default App;
