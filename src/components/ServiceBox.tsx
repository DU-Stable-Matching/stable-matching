import React from 'react'
import { FaBox } from 'react-icons/fa'

const ServiceBox = ({ title, description, buttonText }) => {
    return (
        <div className='space-y-8 text-white'>
            <FaBox color='white' size={30}/>
            <h2>{title}</h2>
            <p>{description}</p>
            <button>{buttonText}</button>
        </div>
    )
}

export default ServiceBox