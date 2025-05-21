import React, { useState, FormEvent, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useUserStore } from "../userState";
import axios from "axios";

interface SignupModalProps {
  show: boolean;
  setShow: React.Dispatch<React.SetStateAction<boolean>>;
}

const SignupModal: React.FC<SignupModalProps> = ({ show, setShow }) => {
  const setUserID = useUserStore((s) => s.setUserID);
  const setUserEmail = useUserStore((s) => s.setEmail);
  const navigate = useNavigate();

  const [userExists, setUserExists] = useState(false);

  const [duId, setDuId] = useState("");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [yearInCollege, setYearInCollege] = useState<number>(0);

  // Prevent background scrolling when modal is open
  useEffect(() => {
    if (show) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [show]);

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const payload = {
      du_id: duId,
      name,
      email,
      password,
      year_in_college: yearInCollege,
    };

    axios
      .post("http://127.0.0.1:8000/api/create_applicant/", payload, {
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        setUserID(response.data.user_id);
        setUserEmail(response.data.email);
        navigate("/user_pref");
      })
      .catch((error) => {
        if (error.response && error.response.status === 400) {
          setUserExists(true);
        } else {
          console.error("An error occurred:", error);
        }
      });
  };

  if (!show) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
      onClick={() => setShow(false)}
      aria-modal="true"
      role="dialog"
    >
      <div
        className="w-full max-w-md bg-white rounded-lg shadow-md p-8 relative"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="text-2xl font-bold text-dark-green mb-6 text-center">
          Sign Up
        </h2>

        {userExists && (
          <div className="mb-4 p-2 bg-red-100 border border-red-400 text-red-700 rounded">
            <p className="text-sm">
              User already exists. Please use a different email or login.
            </p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label htmlFor="duId" className="block text-dark-green mb-1">
              DU ID
            </label>
            <input
              id="duId"
              type="text"
              value={duId}
              onChange={(e) => setDuId(e.target.value)}
              required
              className="w-full border border-cool-gray rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-dark-green"
            />
          </div>

          <div>
            <label htmlFor="name" className="block text-dark-green mb-1">
              Name
            </label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="w-full border border-cool-gray rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-dark-green"
            />
          </div>

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

          <div>
            <label htmlFor="year" className="block text-dark-green mb-1">
              Year in College
            </label>
            <input
              id="year"
              type="number"
              value={yearInCollege}
              onChange={(e) =>
                setYearInCollege(Math.min(Math.max(Number(e.target.value), 0), 5))
              }
              min={0}
              max={5}
              required
              className="w-full border border-cool-gray rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-dark-green"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-dark-green text-white py-2 rounded-lg font-medium hover:bg-myrtle-green transition-colors"
          >
            Sign Up
          </button>
        </form>
        <button
          className="absolute top-3 right-3 text-gray-400 hover:text-gray-700 text-2xl font-bold"
          onClick={() => setShow(false)}
          aria-label="Close"
          type="button"
        >
          &times;
        </button>
      </div>
    </div>
  );
};

export default SignupModal;