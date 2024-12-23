import React from 'react';
import Home from './pages/Home.tsx';
import { Routes, Route } from "react-router-dom";
import Login from './pages/Login.tsx';
import CardSwipe from './pages/CardSwipe.tsx';


function App() {
  return (
    <div>
        <Routes>
          <Route path="/" element={<Home/>}/>
          <Route path="/login" element={<Login/>}/>
          <Route path='/swipe' element={<CardSwipe/>}/>
        </Routes>
    </div>
  );
}

export default App;
