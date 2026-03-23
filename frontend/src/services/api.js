// // const API_BASE_URL = "http://127.0.0.1:8000";
// const API_BASE_URL = "https://astramind-api.onrender.com";

// export const loginUser = async (user_id, password) => {
//   const formData = new URLSearchParams();
//   formData.append("user_id", user_id);
//   formData.append("password", password);

//   const response = await fetch(`${API_BASE_URL}/auth/login`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/x-www-form-urlencoded",
//     },
//     body: formData,
//   });

//   if (!response.ok) {
//     throw new Error("Invalid credentials");
//   }

//   return response.json();
// };












// const API_BASE_URL = "https://astramind-api.onrender.com";

// // -----------------------------
// // LOGIN
// // -----------------------------
// export const loginUser = async (user_id, password) => {

//   const formData = new URLSearchParams();
//   formData.append("user_id", user_id);
//   formData.append("password", password);

//   const response = await fetch(`${API_BASE_URL}/auth/login`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/x-www-form-urlencoded",
//     },
//     body: formData,
//   });

//   const data = await response.json();

//   if (!response.ok) {
//     throw new Error(data.detail || "Invalid credentials");
//   }

//   // ✅ STORE TOKEN HERE
//   localStorage.setItem("token", data.access_token);

//   return data;
// };


// // -----------------------------
// // ASK QUESTION (PROTECTED API)
// // -----------------------------
// export const askQuestion = async (query, session_id = "default") => {

//   const token = localStorage.getItem("token");

//   if (!token) {
//     throw new Error("User not logged in");
//   }

//   const url = `${API_BASE_URL}/api/v1/ask?query=${encodeURIComponent(query)}&session_id=${session_id}`;

//   const response = await fetch(url, {
//     method: "GET",
//     headers: {
//       "Authorization": `Bearer ${token}`,
//       "Content-Type": "application/json",
//     },
//   });

//   const data = await response.json();

//   if (!response.ok) {
//     throw new Error(data.detail || "Error fetching response");
//   }

//   return data;
// };


// // -----------------------------
// // LOGOUT
// // -----------------------------
// export const logoutUser = () => {
//   localStorage.removeItem("token");
// };


// // -----------------------------
// // CHECK AUTH
// // -----------------------------
// export const isAuthenticated = () => {
//   return !!localStorage.getItem("token");
// };

















// const API_BASE_URL = "https://astramind-api.onrender.com";

// // -----------------------------
// // LOGIN
// // -----------------------------
// export const loginUser = async (user_id, password) => {

//   // 🔥 FIX: send RAW body instead of URLSearchParams
//   const body = `user_id=${encodeURIComponent(user_id)}&password=${encodeURIComponent(password)}`;

//   const response = await fetch(`${API_BASE_URL}/auth/login`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/x-www-form-urlencoded",
//     },
//     body: body,
//   });

//   const data = await response.json();

//   if (!response.ok) {
//     throw new Error(data.detail || "Invalid credentials");
//   }

//   // ✅ STORE TOKEN
//   localStorage.setItem("token", data.access_token);

//   return data;
// };


// // -----------------------------
// // ASK QUESTION (PROTECTED API)
// // -----------------------------
// export const askQuestion = async (query, session_id = "default") => {

//   const token = localStorage.getItem("token");

//   if (!token) {
//     throw new Error("User not logged in");
//   }

//   const url = `${API_BASE_URL}/api/v1/ask?query=${encodeURIComponent(query)}&session_id=${session_id}`;

//   const response = await fetch(url, {
//     method: "GET",
//     headers: {
//       "Authorization": `Bearer ${token}`,
//       "Content-Type": "application/json",
//     },
//   });

//   const data = await response.json();

//   if (!response.ok) {
//     throw new Error(data.detail || "Error fetching response");
//   }

//   return data;
// };


// // -----------------------------
// // LOGOUT
// // -----------------------------
// export const logoutUser = () => {
//   localStorage.removeItem("token");
// };


// // -----------------------------
// // CHECK AUTH
// // -----------------------------
// export const isAuthenticated = () => {
//   return !!localStorage.getItem("token");
// };





















// const API_BASE_URL = "https://astramind-api.onrender.com";

// // -----------------------------
// // LOGIN
// // -----------------------------
// export const loginUser = async (user_id, password) => {

//   // ✅ CORRECT WAY (same as Swagger)
//   const formData = new URLSearchParams();
//   formData.append("user_id", user_id);
//   formData.append("password", password);

//   const response = await fetch(`${API_BASE_URL}/auth/login`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/x-www-form-urlencoded",
//     },
//     body: formData,
//   });

//   const data = await response.json();

//   if (!response.ok) {
//     throw new Error(data.detail || "Invalid credentials");
//   }

//   // ✅ Store token
//   localStorage.setItem("token", data.access_token);

//   return data;
// };


// // -----------------------------
// // ASK QUESTION (PROTECTED API)
// // -----------------------------
// export const askQuestion = async (query, session_id = "default") => {

//   const token = localStorage.getItem("token");

//   if (!token) {
//     throw new Error("User not logged in");
//   }

//   const url = `${API_BASE_URL}/api/v1/ask?query=${encodeURIComponent(query)}&session_id=${session_id}`;

//   const response = await fetch(url, {
//     method: "GET",
//     headers: {
//       "Authorization": `Bearer ${token}`,
//       "Content-Type": "application/json",
//     },
//   });

//   const data = await response.json();

//   if (!response.ok) {
//     throw new Error(data.detail || "Error fetching response");
//   }

//   return data;
// };


// // -----------------------------
// // LOGOUT
// // -----------------------------
// export const logoutUser = () => {
//   localStorage.removeItem("token");
// };


// // -----------------------------
// // CHECK AUTH
// // -----------------------------
// export const isAuthenticated = () => {
//   return !!localStorage.getItem("token");
// };















// const API_BASE_URL = "https://astramind-api.onrender.com";

// // -----------------------------
// // LOGIN (FIXED → JSON)
// // -----------------------------
// export const loginUser = async (user_id, password) => {

//   const response = await fetch(`${API_BASE_URL}/auth/login`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json", // ✅ FIX
//     },
//     body: JSON.stringify({
//       user_id: user_id,
//       password: password,
//     }), // ✅ FIX
//   });

//   const data = await response.json();

//   if (!response.ok) {
//     throw new Error(data.detail || "Invalid credentials");
//   }

//   // ✅ Store token
//   localStorage.setItem("token", data.access_token);

//   return data;
// };


// // -----------------------------
// // ASK QUESTION
// // -----------------------------
// export const askQuestion = async (query, session_id = "default") => {

//   const token = localStorage.getItem("token");

//   if (!token) {
//     throw new Error("User not logged in");
//   }

//   const response = await fetch(
//     `${API_BASE_URL}/api/v1/ask?query=${encodeURIComponent(query)}&session_id=${session_id}`,
//     {
//       method: "GET",
//       headers: {
//         "Authorization": `Bearer ${token}`,
//       },
//     }
//   );

//   const data = await response.json();

//   if (!response.ok) {
//     throw new Error(data.detail || "Error fetching response");
//   }

//   return data;
// };


// // -----------------------------
// // LOGOUT
// // -----------------------------
// export const logoutUser = () => {
//   localStorage.removeItem("token");
// };


// // -----------------------------
// // CHECK AUTH
// // -----------------------------
// export const isAuthenticated = () => {
//   return !!localStorage.getItem("token");
// };














const API_BASE_URL = "https://astramind-api.onrender.com";

// -----------------------------
// LOGIN (FINAL FIX)
// -----------------------------
export const loginUser = async (user_id, password) => {

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json", // ✅ MUST BE JSON
    },
    body: JSON.stringify({
      user_id,
      password,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Invalid credentials");
  }

  localStorage.setItem("token", data.access_token);

  return data;
};


// -----------------------------
// ASK QUESTION
// -----------------------------
export const askQuestion = async (query, session_id = "default") => {

  const token = localStorage.getItem("token");

  if (!token) {
    throw new Error("User not logged in");
  }

  const response = await fetch(
    `${API_BASE_URL}/api/v1/ask?query=${encodeURIComponent(query)}&session_id=${session_id}`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Error fetching response");
  }

  return data;
};


// -----------------------------
// LOGOUT
// -----------------------------
export const logoutUser = () => {
  localStorage.removeItem("token");
};


// -----------------------------
// CHECK AUTH
// -----------------------------
export const isAuthenticated = () => {
  return !!localStorage.getItem("token");
};