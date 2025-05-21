import React from 'react'
import Hero from '../components/Hero'
import TopBar from '../components/TopBar'
import Footer from '../components/Footer'
import { BrowserRouter as Router } from 'react-router-dom'
import LowerHome from '../components/LowerHome.js'
import TrustedBy from '../components/TrustedBy'

const Home = () => {
  return (
    <div className="flex flex-col">
      <TopBar/>
      <Hero/>
      <LowerHome/>
      <Footer/>
    </div>
  )
}

export default Home
