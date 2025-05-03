import React from 'react'
import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin } from 'react-icons/fa';

const SocialRow = () => {
    return (
        <div style={{ display: 'flex', justifyContent: 'space-around', color: 'white' }} className='space-x-4'>
            <FaFacebook size={20}/>
            <FaTwitter size={20}/>
            <FaInstagram size={20}/>
            <FaLinkedin size={20}/>
        </div>
    );
}

export default SocialRow;