// import React, { useState } from "react";
// import Login from "./pages/Login";

// function App() {
//   const [isLoggedIn, setIsLoggedIn] = useState(false);

//   return (
//     <div>
//       {!isLoggedIn ? (
//         <Login onLogin={() => setIsLoggedIn(true)} />
//       ) : (
//         <h2 style={{ textAlign: "center", marginTop: "100px" }}>
//           ✅ Logged in successfully (Chat UI coming next)
//         </h2>
//       )}
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