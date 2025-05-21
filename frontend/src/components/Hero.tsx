import React from 'react';
import { Link } from 'react-router-dom';

interface HomeHeroProps {
  setShowSignup: React.Dispatch<React.SetStateAction<boolean>>;
  setShowLogin: React.Dispatch<React.SetStateAction<boolean>>;
}

const Hero: React.FC<HomeHeroProps> = ({ setShowSignup, setShowLogin }) => {
  return (
    <div>
      <div id="home" className="w-full bg-transparent flex flex-col h-[50vh]">
        <div className="invisible md:visible flex justify-between items-center w-full px-8 py-4 md:py-10">
          <div className="text-2xl font-bold text-black">Optimatch</div>
          <div className="flex items-center space-x-4">
            <button onClick={() => setShowSignup(true)} className="px-3 py-1 bg-transparent border-black border-2 text-black rounded-md">
            Sign Up
            </button>
            <button onClick={() => setShowLogin(true)} className="px-3 py-1 bg-black border-white border-2 text-white rounded-md">
            Login
            </button>
          </div>
        </div>
        <div className="flex flex-col items-center justify-between">
          <div className='text-center mt-10 h-[50vh]'>
            <h1 className="text-9xl font-bold text-black font-serif z-30">Let's Match</h1>
          </div>
        </div>

      </div>
    </div>
  );
};

export default Hero;
