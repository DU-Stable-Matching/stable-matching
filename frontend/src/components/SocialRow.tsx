import React from 'react'
import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin } from 'react-icons/fa';

const SocialRow = () => {
    return (
        <div style={{ display: 'flex', justifyContent: 'space-around', color: 'white' }} className='space-x-4'>
            <FaFacebook size={20} color='black'/>
            <FaTwitter size={20} color='black'/>
            <FaInstagram size={20} color='black'/>
            <FaLinkedin size={20} color='black'/>
        </div>
    );
}

export default SocialRow;