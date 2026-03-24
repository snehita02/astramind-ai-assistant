import React, { useState, useRef, useEffect } from "react";
import { askQuestion } from "../services/api"; // ✅ FIX

function Chat({ onLogout }) {
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

    // ✅ Add user message
    setMessages((prev) => [
      ...prev,
      { role: "user", text: currentQuery },
    ]);

    setQuery("");
    setLoading(true);

    try {
      const token = localStorage.getItem("token");

      if (!token) {
        alert("Session expired. Please login again.");
        handleLogout();
        return;
      }

      const response = await fetch(
        `https://astramind-api.onrender.com/api/v1/ask?query=${encodeURIComponent(currentQuery)}&session_id=test`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to fetch response");
      }

      // ✅ Add bot response
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: data.answer,
          sources: data.sources || [],
        },
      ]);

    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: err.message || "Error fetching response." },
      ]);
    }

    setLoading(false);
  };

  // ✅ Logout function
  const handleLogout = () => {
    localStorage.removeItem("token");
    if (onLogout) onLogout();
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>AstraMind</h2>

      {/* ✅ Logout Button */}
      <div style={{ textAlign: "right", marginBottom: "10px" }}>
        <button onClick={handleLogout} style={styles.logoutButton}>
          Logout
        </button>
      </div>

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

              {msg.sources && msg.sources.length > 0 && (
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
  logoutButton: {
    padding: "6px 12px",
    backgroundColor: "#dc3545",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },
  sources: {
    marginTop: "8px",
    fontSize: "12px",
    color: "#333",
  },
};

export default Chat;
