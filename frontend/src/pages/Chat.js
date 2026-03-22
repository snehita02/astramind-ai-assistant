// import React, { useState } from "react";

// function Chat() {
//   const [query, setQuery] = useState("");
//   const [messages, setMessages] = useState([]);

//   const sendMessage = async () => {
//     if (!query) return;

//     const token = localStorage.getItem("token");

//     const response = await fetch(
//       `http://127.0.0.1:8000/api/v1/ask?query=${encodeURIComponent(query)}&session_id=test`,
//       {
//         headers: {
//           Authorization: `Bearer ${token}`,
//         },
//       }
//     );

//     const data = await response.json();

//     setMessages([
//       ...messages,
//       { role: "user", text: query },
//       { role: "bot", text: data.answer, sources: data.sources },
//     ]);

//     setQuery("");
//   };

//   return (
//     <div style={styles.container}>
//       <h2>AstraMind Chat</h2>

//       <div style={styles.chatBox}>
//         {messages.map((msg, index) => (
//           <div key={index} style={styles.message}>
//             <b>{msg.role === "user" ? "You:" : "AstraMind:"}</b> {msg.text}

//             {msg.sources && (
//               <div style={styles.sources}>
//                 <small>Sources:</small>
//                 <ul>
//                   {msg.sources.map((s, i) => (
//                     <li key={i}>{s}</li>
//                   ))}
//                 </ul>
//               </div>
//             )}
//           </div>
//         ))}
//       </div>

//       <div style={styles.inputContainer}>
//         <input
//           value={query}
//           onChange={(e) => setQuery(e.target.value)}
//           placeholder="Ask something..."
//           style={styles.input}
//         />
//         <button onClick={sendMessage} style={styles.button}>
//           Send
//         </button>
//       </div>
//     </div>
//   );
// }

// const styles = {
//   container: {
//     width: "600px",
//     margin: "40px auto",
//     fontFamily: "Arial",
//   },
//   chatBox: {
//     border: "1px solid #ccc",
//     padding: "10px",
//     height: "400px",
//     overflowY: "scroll",
//     marginBottom: "10px",
//   },
//   message: {
//     marginBottom: "10px",
//   },
//   inputContainer: {
//     display: "flex",
//     gap: "10px",
//   },
//   input: {
//     flex: 1,
//     padding: "10px",
//   },
//   button: {
//     padding: "10px",
//     backgroundColor: "#007bff",
//     color: "white",
//     border: "none",
//   },
//   sources: {
//     marginTop: "5px",
//     fontSize: "12px",
//     color: "gray",
//   },
// };

// export default Chat;















import React, { useState, useRef, useEffect } from "react";

function Chat() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  // ✅ Auto scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!query.trim() || loading) return;

    const currentQuery = query;

    setMessages((prev) => [
      ...prev,
      { role: "user", text: currentQuery },
    ]);

    setQuery("");
    setLoading(true);

    try {
      const token = localStorage.getItem("token");

      const response = await fetch(
        `http://127.0.0.1:8000/api/v1/ask?query=${encodeURIComponent(currentQuery)}&session_id=test`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: data.answer,
          sources: data.sources,
        },
      ]);

    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Error fetching response." },
      ]);
    }

    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>AstraMind</h2>

      <div style={styles.chatBox}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              ...styles.messageRow,
              justifyContent:
                msg.role === "user" ? "flex-end" : "flex-start",
            }}
          >
            <div
              style={{
                ...styles.bubble,
                backgroundColor:
                  msg.role === "user" ? "#007bff" : "#e5e5ea",
                color: msg.role === "user" ? "white" : "black",
              }}
            >
              {msg.text}

              {msg.sources && (
                <div style={styles.sources}>
                  <b>Sources:</b>
                  <ul>
                    {msg.sources.map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div style={styles.messageRow}>
            <div style={styles.bubble}>Typing...</div>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      <div style={styles.inputContainer}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask AstraMind..."
          style={styles.input}
          onKeyDown={(e) => {
            if (e.key === "Enter") sendMessage();
          }}
        />

        <button
          onClick={sendMessage}
          style={styles.button}
          disabled={loading}
        >
          Send
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "700px",
    margin: "40px auto",
    fontFamily: "Arial, sans-serif",
  },
  title: {
    textAlign: "center",
    marginBottom: "20px",
  },
  chatBox: {
    height: "500px",
    overflowY: "auto",
    padding: "10px",
    border: "1px solid #ddd",
    borderRadius: "10px",
    backgroundColor: "#f9f9f9",
  },
  messageRow: {
    display: "flex",
    marginBottom: "10px",
  },
  bubble: {
    maxWidth: "70%",
    padding: "10px",
    borderRadius: "10px",
    lineHeight: "1.4",
  },
  inputContainer: {
    display: "flex",
    marginTop: "10px",
    gap: "10px",
  },
  input: {
    flex: 1,
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #ccc",
  },
  button: {
    padding: "12px 20px",
    backgroundColor: "#007bff",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },
  sources: {
    marginTop: "8px",
    fontSize: "12px",
    color: "#333",
  },
};

export default Chat;