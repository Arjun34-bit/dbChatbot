import axios from "axios";
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Spinner from "../Loading/Spinners";
import { URL } from "../constants/constants";
import { ChatState } from "../context/ChatContext";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  // const { userToken, setUserToken } = ChatState();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const response = await axios.post(`${URL}/login`, {
        email,
        password,
      });
      // setUserToken(response.data.token);
      localStorage.setItem("token", response.data.token);
      setLoading(false);
      alert("Login successful!");
      navigate("/chat");
    } catch (error) {
      setLoading(false);
      alert("Login failed: " + error.response.data.message);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="bg-white text-blue-500 p-8 rounded-lg shadow-lg max-w-md w-full">
        <h1 className="text-2xl font-bold mb-6 text-center">Login</h1>
        <form onSubmit={handleLogin}>
          <div className="mb-4">
            <label className="block mb-2">Email</label>
            <input
              type="email"
              className="w-full px-4 py-2 border rounded-lg text-black"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label className="block mb-2">Password</label>
            <input
              type="password"
              className="w-full px-4 py-2 border rounded-lg text-black"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button className="bg-green-500 text-white px-4 py-2 w-full rounded-lg hover:bg-green-600">
            {loading ? (
              <Spinner
                loading={loading}
                size={10}
                color={"#ffff"}
                spinner={"sync"}
              />
            ) : (
              "Login"
            )}
          </button>
        </form>
        <p className="mt-4 text-center">
          Don't have an account?{" "}
          <Link to="/register" className="text-green-300">
            Register
          </Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
