function loadHistory() {
    const historyDiv = document.getElementById("chat-history");
    historyDiv.innerHTML = "";
    const history = JSON.parse(sessionStorage.getItem("chatHistory") || "[]");
    history.forEach(item => {
        const p = document.createElement("p");
        const sender = item.sender === "user" ? "You" : "Assistant";
        p.textContent = `${sender}: ${item.text}`;
        historyDiv.appendChild(p);
    });
    historyDiv.scrollTop = historyDiv.scrollHeight;
}

function addToHistory(sender, text) {
    const history = JSON.parse(sessionStorage.getItem("chatHistory") || "[]");
    history.push({ sender: sender, text: text });
    sessionStorage.setItem("chatHistory", JSON.stringify(history));
    loadHistory();
}

async function sendMessage() {
    const message = document.getElementById("user-input").value;
    const responseDiv = document.getElementById("response");

    addToHistory("user", message);
    responseDiv.innerHTML = "<em>Thinking...</em>";

    const response = await fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `message=${encodeURIComponent(message)}`
    });

    const data = await response.json();
    addToHistory("assistant", data.response);
    responseDiv.textContent = data.response;
    document.getElementById("user-input").value = "";
}

// Enable Enter to send, Shift+Enter to newline
document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.getElementById("user-input");
    loadHistory();

    textarea.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();  // prevent newline
            sendMessage();       // trigger send
        }
    });
});