import React, { use, useState } from 'react'
import Hero from '../components/Hero'
import TopBar from '../components/TopBar'
import Footer from '../components/Footer'
import { BrowserRouter as Router } from 'react-router-dom'
import LowerHome from '../components/LowerHome.js'
import TrustedBy from '../components/TrustedBy'
import LoginModal from '../components/LoginModal'
import SignUpSlice from '../components/SignUpSlice'
import SignupModal from '../components/SignupModal'

const Home = () => {
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);
  console.log(showLogin)

  return (
    <div className="flex flex-col">
      <TopBar setShowLogin={setShowLogin} setShowSignup={setShowSignup}/>
      <Hero setShowSignup={setShowSignup} setShowLogin={setShowLogin}/>
      <LowerHome/>
      <Footer/>
      <LoginModal show={showLogin} setShow={setShowLogin}/>
      <SignupModal show={showSignup} setShow={setShowSignup}/>
    </div>
  )
}

export default Home
