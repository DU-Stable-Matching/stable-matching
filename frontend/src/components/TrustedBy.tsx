import React from 'react'
import LM from '../assets/img/lm.png'
import DU from '../assets/img/du.png'
import USA from '../assets/img/usa.png'


function TrustedBy() {
  return (
    <div className='flex flex-col items-center justify-center opacity-90 mb-24'>
        <h1 className='text-2xl text-center font-bold mt-20'>Trusted by</h1>
        <div className='flex flex-row flex-wrap items-center justify-center mt-10'>
        <img src={LM} className='h-44 mx-10'/>
        <img src={DU} className='h-44 mx-10'/>
        <img src={USA} className='h-44 mx-10'/>
        </div>
    </div>
  )
}

export default TrustedBy
