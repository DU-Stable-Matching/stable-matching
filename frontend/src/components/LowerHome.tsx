import React from 'react'
import BackgroundCanvas from './BackgroundCanvas'
import Placeholder from '../assets/img/ComputerPlaceholder.png'
import PhonePlaceholder from '../assets/img/PhonePlaceholder.png'
import TrustedBy from './TrustedBy'

function LowerHome() {
  return (
    <div className="relative w-full h-full">
      {/* Background directly behind FloatingComputer */}
      <div className="absolute top-0 left-0 w-full h-full -z-10">
        <BackgroundCanvas />
      </div>

      {/* Foreground content */}
      <div className="relative z-10">
         <div className='relative flex mt-48'>
            <div className='rounded-2xl w-[95%] mx-auto flex justify-center h-64 bg-[#8E9C78] z-10' id='thing'>
                  <img src={Placeholder} className='h-[200%] absolute bottom-0 md:flex hidden'/>
                  <img src={PhonePlaceholder} className='h-[140%] absolute bottom-5 md:hidden' />
              </div>
          </div>
        <TrustedBy />
      </div>
    </div>
  );
}

export default LowerHome
