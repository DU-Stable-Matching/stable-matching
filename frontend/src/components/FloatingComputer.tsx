import React from 'react'
import Placeholder from '../assets/img/ComputerPlaceholder.png'
import PhonePlaceholder from '../assets/img/PhonePlaceholder.png'

function FloatingComputer() {
  return (
    <div className='relative flex mt-48'>
       <div className='rounded-2xl w-[95%] mx-auto flex justify-center h-64 bg-[#8E9C78] z-10' id='thing'>
            <img src={Placeholder} className='h-[200%] absolute bottom-0 md:flex hidden'/>
            <img src={PhonePlaceholder} className='h-[140%] absolute bottom-5 md:hidden' />
        </div>
    </div>
  )
}

export default FloatingComputer
