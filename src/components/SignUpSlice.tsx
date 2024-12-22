import React from 'react'

const SignUpSlice = () => {
return (
    <div>
        <div id="contact" className='bg-cool-gray flex w-full min-h-[50vh] justify-center items-center py-12'>
            <div className='mx-8 space-y-4 flex-col md:flex justify-center items-center w-[90%] md:flex-row md:space-y-0 md:space-x-8'>
                <h2 className='text-white text-4xl md:text-5xl font-semibold w-auto md:w-1/2'>Find Your Perfect Student Match</h2>
                <div className='md:flex-row space-y-4 w-full md:w-1/2 justify-between items-center'>
                    <p className='text-white w-full text-lg'>Join our innovative platform today to connect with the best student talent available. Sign up now and take the first step towards optimizing your hiring process.</p>
                    <button className = "px-6 py-3 bg-white border-white border-2 text-black rounded-md">Sign Up</button>
                </div>
            </div>
        </div>
    </div>
)
}

export default SignUpSlice;
