import React from 'react';
import Inspect from "../assets/img/inspect_img.png"

const AboutUs: React.FC = () => (
    <>
        {/* About Block */}
        <div id="about" className="bg-cool-gray flex w-full min-h-screen justify-center items-center">
            <div className="mx-10 space-y-8 flex flex-col justify-center items-center w-[90%]">
                <h2 className="text-white text-4xl md:text-5xl font-semibold">
                    Unlock the potential of student talent with our innovative matching platform.
                </h2>
                <p className="text-white w-full text-lg">
                    Our platform streamlines the hiring process, connecting you with motivated student employees who fit your needs. Experience enhanced productivity and fresh perspectives by tapping into the vibrant student workforce.
                </p>
            </div>
            <div className="w-[70%] items-center hidden md:flex justify-center">
                <img src={Inspect} alt="inspect" />
            </div>
        </div>
    </>
);

export default AboutUs;

