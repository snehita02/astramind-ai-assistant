import React, { useState } from "react";
import { loginUser } from "../services/api";

const Login = ({ onLoginSuccess }) => {

  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      setError("");

      if (!userId || !password) {
        setError("User ID and Password required");
        return;
      }

      await loginUser(userId, password);
      onLoginSuccess();

    } catch (err) {
      setError(err.message || "Invalid credentials");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>AstraMind Login</h1>

      <input
        type="text"
        placeholder="User ID"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        style={{ display: "block", margin: "10px auto", padding: "10px" }}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{ display: "block", margin: "10px auto", padding: "10px" }}
      />

      <button onClick={handleLogin}>
        Login
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default Login;