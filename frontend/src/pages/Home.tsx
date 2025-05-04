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
    </>
  )
}

export default Home
