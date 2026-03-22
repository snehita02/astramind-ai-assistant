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













const API_BASE_URL = "https://astramind-api.onrender.com";

export const loginUser = async (user_id, password) => {

  const formData = new URLSearchParams();
  formData.append("user_id", user_id);
  formData.append("password", password);

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Invalid credentials");
  }

  return data;
};