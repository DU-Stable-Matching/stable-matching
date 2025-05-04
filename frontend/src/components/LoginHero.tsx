import React, { useState, FormEvent, use } from "react";
import { useNavigate } from "react-router-dom";
import { useUserStore } from "../userState.ts";
import axios from "axios";

const LoginScreen: React.FC = () => {
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

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const payload = { du_id: duId, password };
      const loginUrl =
        role === "applicant"
          ? "http://127.0.0.1:8000/api/login/"
          : "http://127.0.0.1:8000/api/login_admin/";

      // 1) Login
      const response = await axios.post(loginUrl, payload, {
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
        },
      });

      console.log("Login response:", response.data);
      // 2) Common setup
      setUserID(response.data.id);
    
      if (role === "applicant") {
        setUserEmail(response.data.email);
        
        
        // 3) Check if they've given prefs
        const { data: hasGivenPrefs } = await axios.get<boolean>(
          `http://127.0.0.1:8000/api/applicant_given_preferences/${response.data.id}`,
        );

        // 4) Store that boolean
        setGivePrefs(hasGivenPrefs);

        // 5) Navigate
        navigate(
          hasGivenPrefs ? "/dashboard" : "/user_pref",
          { replace: true }
        );
      } else {
        // admin
        navigate("/admin_pref", { replace: true });
      }
    } catch (err: any) {
      console.error("Login error:", err);
      if (err.response?.status === 401) {
        setError("Invalid credentials. Please try again.");
      } else {
        setError("Something went wrong. Please try again later.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-periwinkle px-4">
      <div className="w-full max-w-md bg-white rounded-lg shadow-md p-8">
        {/* Role Toggle */}
        <div className="inline-flex border border-dark-green rounded-full overflow-hidden mb-6">
          <button
            type="button"
            onClick={() => setRole("applicant")}
            className={`flex-1 px-4 py-2 font-medium ${
              role === "applicant"
                ? "bg-dark-green text-white"
                : "bg-white text-dark-green"
            }`}
          >
            Applicant
          </button>
          <button
            type="button"
            onClick={() => setRole("admin")}
            className={`flex-1 px-4 py-2 font-medium ${
              role === "admin"
                ? "bg-dark-green text-white"
                : "bg-white text-dark-green"
            }`}
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

          <button
            type="button"
            onClick={() => navigate("/signup")}
            className="w-full bg-white text-dark-green py-2 rounded-lg font-medium border border-dark-green hover:bg-myrtle-green hover:text-white"
          >
            Create an account
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginScreen;
