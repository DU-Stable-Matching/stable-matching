import React, { useState, useEffect } from "react";
import { IoMdLogIn } from "react-icons/io";
import { FaRegEyeSlash, FaRegEye } from "react-icons/fa";
import { MdOutlineCheckBoxOutlineBlank, MdOutlineCheckBox } from "react-icons/md";



import ReactDOM from "react-dom";

const LoginModal = ({ show, onClose, passedEmail="" }) => {
    const [email, setEmail] = useState(passedEmail ? passedEmail : "");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [agree, setAgree] = useState(true);

    const togglePasswordVisibility = () => setShowPassword(!showPassword);

    useEffect(() => {
        const handleEscape = (event: KeyboardEvent) => {
            if (event.key === "Escape") {
                onClose();
            }
        };
        if (show) {
            document.addEventListener("keydown", handleEscape);
        }
        return () => {
            document.removeEventListener("keydown", handleEscape);
        };
    }, [show, onClose]);

    useEffect(() => {
        if (show) {
            document.body.style.overflow = "hidden";
        } else {
            document.body.style.overflow = "auto";
        }
        return () => {
            document.body.style.overflow = "auto";
        };
    }, [show]);

    if (!show) return null;

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log("Do something with the form data with auth");
        if (!agree) {
            console.log("User needs to agree to terms");
        }
        onClose();
    };

    return ReactDOM.createPortal(
        <div className="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center z-50">
            <div className="bg-white rounded-2xl shadow-lg h-[180] w-96">
                <div className="flex flex-col justify-center align-middle items-center px-6 py-6">
                    <IoMdLogIn size={33} />
                    <div className="flex flex-col justify-center items-center space-y-1 text-center">
                        <h2 className="text-2xl font-medium">Create an account</h2>
                        <p className="text-gray-500 text-xs w-11/12">
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi lobortis maximus.
                        </p>
                    </div>
                </div>
                <div className="px-6 py-4">
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label
                                htmlFor="email"
                                className="block text-gray-500 font-light text-xs mb-1"
                            >
                                Email
                            </label>
                            <input
                                type="email"
                                id="email"
                                className="w-full px-2 py-2 h-9 border rounded-lg focus:outline-none focus:ring-2 focus:ring-myrtle-green"
                                placeholder="user@example.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <div>
                            <label
                                htmlFor="password"
                                className="flex justify-between text-gray-500 font-light text-xs mb-1"
                            >
                                Password
                                <div className="flex items-center space-x-1" onClick={togglePasswordVisibility}>
                                    {showPassword ? 
                                        <FaRegEyeSlash/> :
                                        <FaRegEye/> 
                                    }
                                    <p>{showPassword ? "Hide" : "Show"}</p>
                                </div>
                            </label>

                            <div className="flex justify-center items-center align-middle">
                                <input
                                    type={showPassword ? "text" : "password"}
                                    id="password"
                                    className="w-full px-2 h-9 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-myrtle-green"
                                    placeholder="Enter your password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                    
                                />
                            </div>
                            <div onClick={() => setAgree(!agree)} className="flex pt-1 text-gray-500 items-start space-x-1 focus:outline">
                                {agree ? <MdOutlineCheckBoxOutlineBlank size={20}/> : <MdOutlineCheckBox size={20} />}
                                <p style={{fontSize: 10}}>By creating an account, I agree to our Terms of Use and Privacy Policy</p>
                            </div>
                        </div>
                        <button
                            type="submit"
                            className="w-full px-4 py-2 bg-gray-500 text-white rounded-3xl hover:bg-myrtle-green focus:outline-none">
                            Log In
                        </button>
                    </form>
                </div>

                <div className="flex px-6 items-center text-gray-500 justify-center space-x-2">
                    <hr className="flex-grow" />
                    <p>OR</p>
                    <hr className="flex-grow" />
                </div>
                
                <div className="flex justify-center items-center py-4"> {/*  This is a placeholder for Google Sign In, need API */}
                    <img src={require("../assets/img/GooglePlaceholder.png")} alt="google" className="w-10/12"/> 
                </div>
            </div>
        </div>,
        document.getElementById("modal-root") // for the portal, modal-root is in index.html
    );
};

export default LoginModal;
