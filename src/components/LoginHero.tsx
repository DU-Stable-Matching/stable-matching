import React from "react";

const LoginHero = () => {
  const someFunc = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("form submitted");
  };
  return (
    <div className="w-full min-h-screen bg-myrtle-green flex items-center justify-center py-28 px-16">
      {/* white box */}
      <div className="w-screen flex h-fit border-2 border-white items-center justify-center ">
        <div className="flex-col flex-wrap p-12 w-full h-full w-[50%]">
          <div className="flex flex-wrap mb-5">
            <h1 className="text-6xl font-bold mb-4 text-white">
              Welcome Back! Please Log In
            </h1>
            <p className="text-white text- leading-7 ">
              Access your account to connect with potential employers and find
              the perfect job.
            </p>
          </div>
          <form onSubmit={someFunc}>
            <input
              className="bg-myrtle-green text-white placeholder-white p-3 text-base leading-7 rounded-lg border-2 mr-4 "
              type="text"
              placeholder="Username or Email"
              name=""
              id=""
            />
            <button
              className=" text-black bg-white py-3 px-6 rounded-lg my-4 leading-7"
              type="submit"
            >
              Login
            </button>
          </form>
        </div>
        <div className="w-full h-full p-3 items-center hidden md:flex">
          <img
            className="w-full h-full"
            src={require("../assets/img/Welcome_aboard.png")}
            alt="Welcome aboard"
          />
        </div>
      </div>
    </div>
  );
};

export default LoginHero;
