import React from 'react'

const Hero = () => {
  return (
    <div className="w-full h-[90vh] bg-myrtle-green flex items-center justify-center">
        <div className="flex justify-between items-center w-full max-w-6xl">
            <div className="mx-8 w-[40%] flex flex-col text-white space-y-6">
                <h2 className='text-3xl md:text-5xl'>Find Your Ideal Student Employee Today</h2>
                <p>Unlock the potential of your business by connecting with talented students eager to contribute. Our advanced algorithms ensure the perfect match for your employment needs.</p>
                <div className="space-x-4 flex">
                    <button className = "px-6 py-3 bg-transparent border-white border-2 text-white rounded-md"> Get Started </button>
                    <button className = "px-6 py-3 bg-white border-white border-2 text-dark-green rounded-md"> Learn More </button>
                </div>
            </div>
            <div className="w-[40%] items-center">
                <img className="w-full " src={require("/Users/denverpersinger/stable-matching/src/assets/img/home_img.png")} alt="Home"/>
            </div>
        </div>
    </div>
  )
}

export default Hero
