// import React from "react";

// function App() {
//   return (
//     <div style={{ padding: "20px", fontFamily: "Arial" }}>
//       <h1>AstraMind Frontend</h1>
//       <p>Frontend setup successful 🚀</p>
//     </div>
//   );
// }

// export default App;








import React, { useState } from "react";
import Login from "./pages/Login";
import Chat from "./pages/Chat";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <div>
      {!isLoggedIn ? (
        <Login onLogin={() => setIsLoggedIn(true)} />
      ) : (
        <Chat />
      )}
    </div>
  );
}

export default App;