import React, { useState } from 'react';
import { FaBars } from 'react-icons/fa';
import { Link } from 'react-router-dom';

const TopBar = () => {
    const [show, setShow] = useState(false);
    return (
        <div className="fixed w-full z-50">
            <div className="bg-dark-green flex justify-between px-12 h-14">
                <Link to="/" className="flex items-center text-white">
                    <h1 className="text-xl font-semibold">OptiMatch</h1>
                </Link>
                <div className="flex items-center">
                    <ul className="hidden lg:flex px-8 text-white">
                        <li>
                            <Link to="/">Home</Link>
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
                    {show && (
                        <div className="overflow-y-hidden w-full pt-24 lg:hidden absolute left-0 top-0 h-screen text-white bg-dark-green flex-col justify-between">
                            <div className="flex justify-center lg:hidden z-10 pb-10 cursor-pointer" onClick={() => setShow(!show)}>
                                <FaBars size={20} color="white" />
                            </div>
                            <ul className="text-center flex-col w-full h-full space-y-4">
                                <li className="text-2xl font-semibold" onClick={() => setShow(!show)}>
                                    <a href="#home">Home</a>
                                </li>
                                <li className="text-2xl font-semibold" onClick={() => setShow(!show)}>
                                    <a href="#about">About Us</a>
                                </li>
                                <li className="text-2xl font-semibold" onClick={() => setShow(!show)}>
                                    <a href="#contact">Contact</a>
                                </li>
                                <li className="text-2xl font-semibold" onClick={() => setShow(!show)}>
                                    <a href="#services">Services</a>
                                </li>
                            </ul>
                        </div>
                    )}
                    <div className="flex items-center space-x-4">
                        {!show && (
                            <div className="lg:hidden z-10 cursor-pointer" onClick={() => setShow(!show)}>
                                <FaBars size={20} color="white" />
                            </div>
                        )}
                        <Link to="/signup" className="px-3 py-1 bg-transparent border-white border-2 text-white rounded-md">
                            Sign Up
                        </Link>
                        <Link to="/login" className="px-3 py-1 bg-white border-white border-2 text-dark-green rounded-md">
                            Login
                        </Link>
                    </div>
                </div>
            </div>
            <hr className="border-white border-1 w-full" />
        </div>
    );
};

export default TopBar;
