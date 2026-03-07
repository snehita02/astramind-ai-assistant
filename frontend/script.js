const API_URL = "https://astramind-api.onrender.com/api/v1/ask";

function appendMessage(text, type) {

const chat = document.getElementById("chat-container");

const message = document.createElement("div");

message.className = "message " + type;

message.innerHTML = text;

chat.appendChild(message);

chat.scrollTop = chat.scrollHeight;

}

async function sendMessage() {

const input = document.getElementById("user-input");
const department = document.getElementById("department").value;

const query = input.value;

if (!query) return;

appendMessage("You: " + query, "user");

input.value = "";

const url = `${API_URL}?query=${encodeURIComponent(query)}&department=${department}&session_id=web-session`;

try {

const response = await fetch(url);

const data = await response.json();

const answerBlock = `
<b>AstraMind:</b> ${data.answer}

<div class="meta">
Confidence: ${data.confidence}
<br>
Grounded: ${data.grounded}
<br>
Evaluation: ${data.evaluation}
</div>
`;

appendMessage(answerBlock, "ai");

} catch (error) {

appendMessage("Error connecting to backend.", "ai");

}

}