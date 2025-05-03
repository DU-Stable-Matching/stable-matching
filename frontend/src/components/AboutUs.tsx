import React from 'react'
import ServiceBox from './ServiceBox.tsx'

const AboutUs = () => {
return (
    <div>
        <div id="services" className='bg-cool-gray w-full min-h-screen flex justify-center items-center'>
            <div className="flex-col space-y-24 py-12">
            <div className='mx-10 space-y-4 flex-col md:flex justify-center items-center w-[90%] md:flex-row md:space-y-0 md:space-x-8'>
                <h2 className='text-white text-4xl md:text-5xl font-semibold w-auto md:w-1/2'>Discover the key features that make our matching service exceptional.</h2>
                <p className='text-white w-full md:w-1/2 text-lg'>Our Advanced Matching Algorithm ensures that you find the perfect fit for your needs. By analyzing various factors, it connects employers with the most suitable student candidates. Experience a seamless hiring process that saves you time and effort.</p>
            </div>
            <div className='flex flex-col md:flex-row w-[90%] justify-center items-center mx-12 space-y-12 md:space-y-0 md:space-x-12'>
                <ServiceBox title={"Access a vast database of diverse student profiles tailored for your needs."} description={"Our Wide Student Profiles Database allows you to explore a variety of talents."} buttonText={"Learn More"}/>
                <ServiceBox title={"Navigate effortlessly with our intuitive and user-friendly interface."} description={"Our Easy-to-Use Interface makes the hiring process straightforward and efficient."} buttonText={"Sign Up"}/>
                <ServiceBox title={"Experience the future of student employment with our innovative platform."} description={"Join us today and transform your hiring experience."} buttonText={"Get Started"}/>
            </div>
            </div>
        </div>

        <div id="about" className='bg-myrtle-green flex w-full min-h-screen justify-center items-center'>
            <div className='mx-10 space-y-8 flex flex-col justify-center items-center w-[90%]'>
                <h2 className='text-white text-4xl md:text-5xl font-semibold'>Unlock the potential of student talent with our innovative matching platform.</h2>
                <p className='text-white w-full text-lg'>Our platform streamlines the hiring process, connecting you with motivated student employees who fit your needs. Experience enhanced productivity and fresh perspectives by tapping into the vibrant student workforce.</p>
            </div>
            <div className="w-[70%] items-center hidden md:flex justify-center">
                <img src={require("../assets/img/inspect_img.png")} alt="inspect"/>
            </div>
        </div>
    </div>
)
}

export default AboutUs
