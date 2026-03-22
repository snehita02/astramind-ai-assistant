// import React, { useState } from "react";
// import { loginUser } from "../services/api";

// function Login({ onLogin }) {
//   const [userId, setUserId] = useState("");
//   const [password, setPassword] = useState("");
//   const [error, setError] = useState("");

//   const handleLogin = async () => {
//     try {
//       const data = await loginUser(userId, password);

//       // Save token
//       localStorage.setItem("token", data.access_token);

//       onLogin(); // move to chat
//     } catch (err) {
//       setError("Invalid credentials");
//     }
//   };

//   return (
//     <div style={styles.container}>
//       <h2>AstraMind Login</h2>

//       <input
//         type="text"
//         placeholder="User ID"
//         value={userId}
//         onChange={(e) => setUserId(e.target.value)}
//         style={styles.input}
//       />

//       <input
//         type="password"
//         placeholder="Password"
//         value={password}
//         onChange={(e) => setPassword(e.target.value)}
//         style={styles.input}
//       />

//       <button onClick={handleLogin} style={styles.button}>
//         Login
//       </button>

//       {error && <p style={styles.error}>{error}</p>}
//     </div>
//   );
// }

// const styles = {
//   container: {
//     width: "300px",
//     margin: "100px auto",
//     display: "flex",
//     flexDirection: "column",
//     gap: "10px",
//     textAlign: "center",
//   },
//   input: {
//     padding: "10px",
//     fontSize: "14px",
//   },
//   button: {
//     padding: "10px",
//     backgroundColor: "#007bff",
//     color: "white",
//     border: "none",
//     cursor: "pointer",
//   },
//   error: {
//     color: "red",
//   },
// };

// export default Login;


















import React, { useState, useEffect } from "react";
import { loginUser, isAuthenticated } from "./api";

const Login = ({ onLoginSuccess }) => {

  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // ✅ Auto login if token exists
  useEffect(() => {
    if (isAuthenticated()) {
      onLoginSuccess();
    }
  }, []);

  const handleLogin = async () => {
    try {
      setError("");
      await loginUser(userId, password);
      onLoginSuccess();
    } catch (err) {
      setError(err.message);
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

      <button
        onClick={handleLogin}
        style={{ padding: "10px 20px", backgroundColor: "#007bff", color: "white" }}
      >
        Login
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default Login;