import React from 'react'
import SocialRow from './SocialRow'
import Policies from './Policies'

const Footer = () => {
  return (
    <div className='bg-transparent flex-col w-full min-h-[30vh] py-12'>
        <div className="justify-center flex w-full items-center px-8">
            <hr className="border-black border-1 w-full" />
        </div>
        <div className='justify-between flex w-full p-8 items-center'>
            <h2 className='text-lg text-black'>OptiMatch</h2>
            <ul className="hidden lg:flex px-8 text-black font-semibold">
                <li> 
                    <a href="#home">Home</a>
                </li>
                <li> 
                    <a href="#about">About Us</a>
                </li>
                <li> 
                    <a href="#contact">Contact</a>
                </li>
                <li> 
                    <a href="#services">Services</a>
                </li>
            </ul>
            <SocialRow />
        </div>
        <div className="justify-center flex w-full items-center px-8">
            <hr className="border-black border-1 w-full" />
        </div>
        <div>
            <Policies/>
        </div>
    </div>
  )
}

export default Footer