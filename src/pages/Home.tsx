import React from 'react'
import Hero from '../components/Hero.tsx'
import TopBar from '../components/TopBar.tsx'
import AboutUs from '../components/AboutUs.tsx'
import SignUpSlice from '../components/SignUpSlice.tsx'
import Footer from '../components/Footer.tsx'
import { BrowserRouter as Router } from 'react-router-dom'

const Home = () => {
  return (
    <>
      <TopBar/>
      <Hero/>
      <AboutUs/>
      <SignUpSlice/>
      <Footer/>
      {
         const url = "https://example.org/products.json";
         try {
           const response = await fetch(url);
           if (!response.ok) {
             throw new Error(`Response status: ${response.status}`);
           }
       
           const json = await response.json();
           console.log(json);
         } catch (error) {
           console.error(error.message);
         }
      }
    </>
  )
}

export default Home
