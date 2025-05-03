import React, { useState, FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useUserStore } from "../userState.ts";

const LoginScreen: React.FC = () => {
  const setUserID = useUserStore((s) => s.setUserID);
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // 1) set your userID in the store
    setUserID(1);

    // 2) navigate _after_ your store is updated
    navigate("/user_pref", { replace: true });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-periwinkle px-4">
      <div className="w-full max-w-md bg-white rounded-lg shadow-md p-8">
        <h2 className="text-2xl font-bold text-dark-green mb-6 text-center">
          Log In
        </h2>
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label htmlFor="email" className="block text-dark-green mb-1">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full border border-cool-gray rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-dark-green"
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-dark-green mb-1">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full border border-cool-gray rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-dark-green"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-dark-green text-white py-2 rounded-lg font-medium hover:bg-myrtle-green transition-colors"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginScreen;
