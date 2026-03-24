const API_BASE_URL = "https://astramind-api.onrender.com";

// -----------------------------
// LOGIN (FIXED FOR FASTAPI FORM)
// -----------------------------
export const loginUser = async (user_id, password) => {

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      user_id,
      password,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    let errorMessage = "Invalid credentials";

    if (Array.isArray(data.detail)) {
      errorMessage = data.detail.map(e => e.msg).join(", ");
    } else if (typeof data.detail === "string") {
      errorMessage = data.detail;
    }

    throw new Error(errorMessage);
  }

  localStorage.setItem("token", data.access_token);

  return data;
};


// -----------------------------
// ASK QUESTION (KEEP SAME)
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
    let errorMessage = "Error fetching response";

    if (Array.isArray(data.detail)) {
      errorMessage = data.detail.map(e => e.msg).join(", ");
    } else if (typeof data.detail === "string") {
      errorMessage = data.detail;
    }

    throw new Error(errorMessage);
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