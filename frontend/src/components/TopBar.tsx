import React, { useState } from 'react';
import { FaBars } from 'react-icons/fa';
import { Link } from 'react-router-dom';

const TopBar = () => {
    const [show, setShow] = useState(false);
    return (
        <div className="fixed w-full z-50 justify-center flex pointer-events-none">
            {/* Regular TopBar */}
            <div className="bg-white/50 backdrop-blur-md hidden md:flex justify-center my-8 px-4 h-14 w-[124] rounded-full pointer-events-auto">
                <div className="flex items-center">
                    <ul className="hidden md:flex text-black font-bold">
                        <li>
                            <Link to="/">Home</Link>
                        </li>
                        <li>
                           <Link to="/#about">About Us</Link>
                        </li>
                        <li>
                            <Link to="/#contact">Contact</Link>
                        </li>
                        <li>
                            <Link to="/#services">Services</Link>
                        </li>
                    </ul>
                </div>
            </div>

            {/* Mobile Menu */}
            <div className='flex md:hidden z-10 cursor-pointer pointer-events-auto bg-white w-full h-16 shadow-lg' onClick={() => setShow(!show)}>
                {!show && (
                <div className='flex flex-row-reverse w-full justify-between align-middle m-4'>
                    <FaBars size={20} color="black" />
                    <div className="text-2xl font-bold text-black">Optimatch</div>
                </div>
                )}
            </div>
            {show && (
                <div className="overflow-y-hidden pointer-events-auto w-full pt-24 md:hidden flex absolute left-0 top-0 h-screen text-black bg-white flex-col justify-center align-center">
                    <div className="flex justify-center md:hidden z-10 pb-10 cursor-pointer" onClick={() => setShow(!show)}>
                        <FaBars size={20} color="black" />
                    </div>
                    <ul className="text-center flex-col w-full h-full space-y-4">
                        <li className="text-2xl font-semibold" onClick={() => setShow(!show)}>
                             <Link to="/">Home</Link>
                        </li>
                        <li className="text-2xl font-semibold" onClick={() => setShow(!show)}>
                            <Link to="/#about">About Us</Link>
                        </li>
                        <li className="text-2xl font-semibold" onClick={() => setShow(!show)}>
                            <Link to="/#contact">Contact</Link>
                        </li>
                        <li className="text-2xl font-semibold" onClick={() => setShow(!show)}>
                           <Link to="/#services">Services</Link>
                        </li>
                    </ul>
                </div>
            )}
        </div>
    );
};

export default TopBar;
