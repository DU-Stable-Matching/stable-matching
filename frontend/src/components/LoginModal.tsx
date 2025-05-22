import React, { useState, FormEvent, use } from "react";
import { useNavigate } from "react-router-dom";
import { useUserStore } from "../userState";
import axios from "axios";

interface LoginModalProps {
  show: boolean;
  setShow: React.Dispatch<React.SetStateAction<boolean>>;
}

const LoginModal: React.FC<LoginModalProps> = ({ show, setShow }) => {
  const setUserID        = useUserStore((s) => s.setUserID);
  const setUserEmail     = useUserStore((s) => s.setEmail);
  const setGivePrefs     = useUserStore((s) => s.setGivePrefrences);
  const userID           = useUserStore(state => state.userID);
  const navigate         = useNavigate();

  const [duId, setDuId]         = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole]         = useState<"admin" | "applicant">("applicant");
  const [error, setError]       = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Disable scrolling when modal is open
  React.useEffect(() => {
    if (show) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [show]);

  const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      setShow(false);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const payload = { du_id: duId, password };
      const loginUrl =
        role === "applicant"
          ? "http://127.0.0.1:8000/api/login/"
          : "http://127.0.0.1:8000/api/admin_login/";

      const prefsUrl =
        role === "applicant"
          ? "http://127.0.0.1:8000/api/applicant_given_preferences/"
          : "http://127.0.1:8000/api/admin_given_preferences/";

      // 1) Login
      const response = await axios.post(loginUrl, payload, {
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
        },
      });

      setUserID(response.data.id);
      setUserEmail(response.data.email);

      // 3) Check if they've given prefs
      const { data: hasGivenPrefs } = await axios.get<boolean>(
        prefsUrl + response.data.id,
      );

      setGivePrefs(hasGivenPrefs);

      if (role === "applicant") {
        if (hasGivenPrefs) {
          navigate("/dashboard", { replace: true });
        } else {
          navigate("/user_pref", { replace: true });
        }
      } else if (role === "admin") {
        if (hasGivenPrefs) {
          navigate("/admin_dashboard", { replace: true });
        } else {
          navigate("/admin_pref", { replace: true });
        }
      }
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError("Invalid credentials. Please try again.");
      } else {
        setError("Something went wrong. Please try again later.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (!show) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
      onClick={handleBackdropClick}
      style={{ transition: "background 0.2s" }}
    >
      <div
        className="w-full max-w-md bg-white rounded-lg shadow-md p-8 relative"
        onClick={e => e.stopPropagation()}
      >
        {/* Role Toggle */}
        <div className="relative inline-flex border border-dark-green rounded-full overflow-hidden mb-6 w-3/4 max-w-xs mx-auto">
          <span
            className="absolute top-0 left-0 h-full w-1/2 transition-transform duration-300 ease-in-out bg-dark-green rounded-full z-0"
            style={{
              transform: role === "admin" ? "translateX(100%)" : "translateX(0%)",
            }}
            aria-hidden="true"
          />
          <button
            type="button"
            onClick={() => setRole("applicant")}
            className={`relative z-10 flex-1 px-4 py-2 font-medium transition-colors duration-300 ${
              role === "applicant"
          ? "text-white"
          : "text-dark-green"
            }`}
            style={{ outline: "none" }}
          >
            Applicant
          </button>
          <button
            type="button"
            onClick={() => setRole("admin")}
            className={`relative z-10 flex-1 px-4 py-2 font-medium transition-colors duration-300 ${
              role === "admin"
          ? "text-white"
          : "text-dark-green"
            }`}
            style={{ outline: "none" }}
          >
            Administrator
          </button>
        </div>

        <h2 className="text-2xl font-bold text-dark-green mb-6 text-center">
          {role === "admin" ? "Admin Login" : "Applicant Login"}
        </h2>

        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            <p className="text-sm">{error}</p>
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
            disabled={isLoading}
            className="w-full bg-dark-green text-white py-2 rounded-lg font-medium hover:bg-myrtle-green disabled:bg-gray-400"
          >
            {isLoading ? "Logging in..." : "Login"}
          </button>
        </form>
        {/* Close button (optional) */}
        <button
          className="absolute top-2 right-2 text-gray-400 hover:text-gray-600 text-2xl"
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

export default LoginModal;
